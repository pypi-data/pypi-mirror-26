import os
from collections import defaultdict

import numpy as np
import qcodes
import qcodes.data.location

from pysweep.data_storage.base_storage import BaseStorage
from pysweep.utils import DictMerge


class SpyviewMetaWriter:
    def __init__(self, writer_function):

        self._writer_function = writer_function
        self._default_axis_properties = dict(max=0, min=np.inf, step=-1, length=1, name="")
        self._axis_properties = defaultdict(lambda: dict(self._default_axis_properties))

    def add(self, spyview_buffer, independent_parameters):

        property_names = ["length", "min", "max", "name"]
        property_values = []
        update = False
        previous_axis_length = 1
        for param in independent_parameters:

            value = spyview_buffer[param]["value"]
            mx = max(value)
            mn = min(value)

            if self._axis_properties[param]["max"] < mx:
                self._axis_properties[param]["max"] = mx
                update = True
            else:
                mx = self._axis_properties[param]["max"]

            if self._axis_properties[param]["min"] > mn:
                self._axis_properties[param]["min"] = mn
                update = True
            else:
                mn = self._axis_properties[param]["min"]

            self._axis_properties[param]["step"] = value[previous_axis_length] - value[0]
            self._axis_properties[param]["name"] = param

            self._axis_properties[param]["length"] = int((mx - mn) / self._axis_properties[param]["step"]) + 1
            previous_axis_length = self._axis_properties[param]["length"]

            s = "\n".join(str(self._axis_properties[param][k]) for k in property_names)
            property_values.append(s)
            property_names = ["length", "max", "min", "name"]

        if not update:
            return

        if len(independent_parameters) < 3:
            property_values.append("1\n0\n1\nnone")

        out = "\n".join(property_values)
        self._writer_function(out)


class SpyviewWriter:
    """
    Save measurement results as spyview files
    """

    def __init__(self, writer_function, meta_writer, delayed_parameters=None, max_buffer_size=1000):
        """
        Parameters
        ----------
        writer_function: callable
        delayed_parameters: list, str
            A list of delayed parameters
        max_buffer_size: int
            If the number of lines to be written to the output file exceeds this number, the buffered values will be
            written to the file system.
        """

        self._max_buffer_size = max_buffer_size
        self._delayed_parameters = delayed_parameters or []
        self._writer_function = writer_function

        self._buffer = dict()
        self._merger = DictMerge(unit="replace", value="append", independent_parameter="replace")
        self._inner_sweep_start_value = None
        self._independent_parameters = []
        self._meta_writer = meta_writer

    def _get_buffer_size(self):
        if self._buffer == dict():
            return 0

        size = np.inf
        for p in self._buffer.values():
            value = p["value"]
            if hasattr(value, "__len__"):
                this_size = len(value)
            else:
                this_size = 1

            size = min([size, this_size])
        return size

    def _find_independent_parameters(self):

        def telescope_collapse(lst):
            b = [lst[0]]

            for l in lst[1:]:
                if l != b[-1]:
                    b.append(l)

            return len(b)

        independent_collapsed = [(k, telescope_collapse(self._buffer[k]["value"])) for k in self._buffer
                                  if "independent_parameter" in self._buffer[k]]

        s = sorted(independent_collapsed, key=lambda el: el[1], reverse=True)
        return list(zip(*s))[0]

    def _write_buffer(self):

        # We will first write the independent parameters in the right order
        if len(self._independent_parameters) == 0:
            self._independent_parameters = self._find_independent_parameters()

        buffer_values = [self._buffer[param]["value"] for param in self._independent_parameters]

        # The rest of the variables
        buffer_values.extend([self._buffer[param]["value"] for param in self._buffer.keys() if param not
                              in self._independent_parameters])

        inner_sweep_values = np.array(buffer_values[0])

        if self._inner_sweep_start_value is None:
            self._inner_sweep_start_value = inner_sweep_values[0]

        block_indices = inner_sweep_values == self._inner_sweep_start_value
        escapes = [{True: "\n\n", False: "\n"}[i] for i in block_indices]
        escapes = escapes[1:] + ['\n']

        lines = ["\t".join([str(ii) for ii in i]) for i in zip(*buffer_values)]
        lines = ["{}{}".format(*i) for i in zip(lines, escapes)]
        out = "".join(lines)

        self._writer_function(out)
        self._meta_writer.add(self._buffer, self._independent_parameters)
        self._buffer = dict()

    def add(self, dictionary):
        delayed_params_buffer = {param: {"value": []} for param in self._delayed_parameters}

        self._buffer = self._merger.merge([dictionary, delayed_params_buffer, self._buffer])
        if self._get_buffer_size() >= self._max_buffer_size:
            self._write_buffer()

    def finalize(self):
        if self._get_buffer_size() >= 2:
            self._write_buffer()


class SpyviewStorage(BaseStorage):
    @staticmethod
    def default_file_path():
        io = qcodes.DiskIO('.')
        home_path = os.path.expanduser("~")
        data_path = os.path.join(home_path, "data", "{date}", "{date}_{counter}.dat")
        loc_provider = qcodes.data.location.FormatLocation(fmt=data_path)
        file_path = loc_provider(io)

        dir_name, _ = os.path.split(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        return file_path

    @staticmethod
    def default_meta_file_path(output_file_path):
        dirname, filename = os.path.split(output_file_path)
        meta_file_name = filename.replace(".dat", ".meta.txt")
        return os.path.join(dirname, meta_file_name)

    def __init__(self, output_file_path=None, delayed_parameters=None, max_buffer_size=1000):

        self._output_file_path = output_file_path or SpyviewStorage.default_file_path()
        self._output_meta_file_path = SpyviewStorage.default_meta_file_path(self._output_meta_file_path)

        self._meta_writer = SpyviewMetaWriter(self._meta_writer_function)
        self._writer = SpyviewWriter(
            self._writer_function,
            self._meta_writer,
            delayed_parameters=delayed_parameters,
            max_buffer_size=max_buffer_size
        )

    def _meta_writer_function(self, output):
        with open(self._output_meta_file_path, "w") as fh:
            fh.write(output)

    def _writer_function(self, output):
        with open(self._output_file_path, "a") as fh:
            fh.write(output)

    def add(self, dictionary):
        self._writer.add(dictionary)

    def output(self):
        return self._output_file_path

    def finalize(self):
        self._writer.finalize()




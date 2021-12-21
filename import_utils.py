import itertools as it
import pathlib as pl
import re
from typing import Tuple, Union

import numpy as np


def import_header(folder: Union[str, pl.Path] = "", file_name: str = "") -> dict:
    path = pl.Path(folder, file_name)

    # Import header
    header = ""
    header_size = 1

    with open(path, "r") as file:
        for _ in range(header_size):
            header += (
                file.readline().rstrip().lstrip().strip("#").strip().replace(" ", "")
            )
        # Split only on "," if not inside []
        header = re.split(r",(?![^\[]*\])", header)

    header_dict = {}
    for item in header:
        splitted_item = item.split("=")
        if splitted_item[0] == "f":
            header_dict[splitted_item[0]] = np.complex(splitted_item[1])
        elif splitted_item[0] == "forcing":
            header_dict[splitted_item[0]] = np.complex(splitted_item[1])
        elif splitted_item[1] == "None":
            header_dict[splitted_item[0]] = None
        else:
            try:
                header_dict[splitted_item[0]] = float(splitted_item[1])
            except:
                header_dict[splitted_item[0]] = splitted_item[1]

    return header_dict


def import_data(
    file_name: pl.Path,
    start_line: int = 0,
    max_lines: int = None,
    step: int = 1,
    dtype=None,
) -> Tuple[np.ndarray, dict]:

    # Import header
    header_dict = import_header(file_name=file_name)

    # Set dtype if not given as argument
    if dtype is None:
        dtype = np.float64

    stop_line = None if max_lines is None else start_line + max_lines
    # Import data
    with open(file_name) as file:
        # Setup iterator
        line_iterator = it.islice(
            file,
            start_line,
            stop_line,
            step,
        )
        data_in: np.ndarray(dtype=dtype) = np.genfromtxt(
            line_iterator, dtype=dtype, delimiter=","
        )

    if data_in.size == 0:
        raise ImportError(
            "No data was imported; file contained empty lines. "
            + f"File_name = {file_name}"
        )

    if len(data_in.shape) == 1:
        data_in = np.reshape(data_in, (1, data_in.size))

    return data_in, header_dict

import os
import pathlib as pl
import numpy as np


def count_existing_files_or_dirs(search_path="", search_pattern="*.csv"):
    """Counts the number of files or folder of a specific kind, and returns the
    the count. To be used to store numbered folders/files in a numbered order."""

    search_path = pl.Path(search_path)

    # Check if path exists
    seach_path_exists = os.path.isdir(search_path)
    if seach_path_exists:
        if search_pattern != "/":
            n_files = len(list(search_path.glob(search_pattern)))
        else:
            dirs = list(search_path.glob("*"))
            dirs = [dirs[i] for i in range(len(dirs)) if os.path.isdir(dirs[i])]
            n_files = len(dirs)
    else:
        n_files = 0

    return n_files


def get_dirs_in_path(path: pl.Path, recursively=False) -> list:
    """Get sorted dirs in path

    Parameters
    ----------
    path : pl.Path
        The path to search for dirs
    recursively : bool
        Whether to search for dirs recursively or not

    Returns
    -------
    list
        The dirs contained in path
    """

    if recursively:
        dirs = list(path.rglob("*"))
    else:
        dirs = list(path.glob("*"))

    # Filter out anything else than directories
    dirs = [dirs[i] for i in range(len(dirs)) if dirs[i].is_dir()]

    # Sort dirs
    dirs = [dirs[i] for i in np.argsort(dirs)]

    return dirs


def get_files_in_path(
    path: pl.Path,
    search_pattern: str = "*.csv",
    filter_out_pattern: str = "",
    recursively: bool = False,
) -> list:
    """Get sorted files in path

    Parameters
    ----------
    path : pl.Path
        The path to search for files

    Returns
    -------
    list
        The files contained in path
    """
    if recursively:
        files = list(path.rglob(search_pattern))
    else:
        files = list(path.glob(search_pattern))

    # Filter out dirs
    files = [files[i] for i in range(len(files)) if not files[i].is_dir()]
    # Filter out files that contains filter_out_pattern
    if len(filter_out_pattern) > 0:
        files = [
            files[i]
            for i in range(len(files))
            if filter_out_pattern not in str(files[i])
        ]
    # Sort files
    files = [files[i] for i in np.argsort(files)]

    return files


def get_file_names_in_path(path: pl.Path, search_pattern: str = "*.csv") -> list:
    """Get the names of the files in a path

    Parameters
    ----------
    path : pl.Path
        The path to search for files
    search_pattern : str, optional
        The search pattern, by default "*.csv"

    Returns
    -------
    list
        The names of the files in the path
    """

    # Try finding files from exp_folder only
    files = get_files_in_path(path, search_pattern=search_pattern)
    names = [file.name for file in files]

    return names


def generate_dir(expected_path, subfolder=""):
    """Generate a directory from a path and possibly a subfolder

    Parameters
    ----------
    expected_path : str, Path
        Path to the dir
    subfolder : str, optional
        Subfolder to append to the path

    """

    if len(subfolder) == 0:
        # See if folder is present
        dir_exists = os.path.isdir(expected_path)

        if not dir_exists:
            os.makedirs(expected_path)

    else:
        # Check if path exists
        expected_path = str(pl.Path(expected_path, subfolder))
        dir_exists = os.path.isdir(expected_path)

        if not dir_exists:
            os.makedirs(expected_path)

    return expected_path

"""
A module that contains utility function mainly used for operations in the
missing from the pathlib module.
"""

import os
import pathlib
import shutil


def get_directory_contents(directory):
    """
    return a sorted list of the contents of a directory
    """
    contents = []

    for child in directory.iterdir():
        contents.append(child)

    return sorted(contents)


def rmtree(tree):
    """
    a wrapper around shutil.rmtree to recursively delete a directory specified
    by a pathlib.Path object
    """
    shutil.rmtree(str(tree))


def is_same_file(file1, file2):
    """
    test if two pathlib.Path() objects are the same file

    NOTE: python 3.5 supports pathlib.Path.samefile(file)
    NOTE: this can raise exception FileNotFoundError
    """
    return file1.resolve() == file2.resolve()


def is_same_files(files1, files2):
    """
    test if two collection of files are equivalent
    """
    files1_resolved = [f.resolve() for f in files1]
    files2_resolved = [f.resolve() for f in files2]
    return files1_resolved == files2_resolved


def get_absolute_path(file):
    """
    get the absolute path of a pathlib.Path() object
    """
    absolute_path = os.path.abspath(os.path.expanduser(str(file)))
    return pathlib.Path(absolute_path)


def get_relative_path(path, start_at):
    """
    get the relative path of a pathlib.Path() object

    NOTE: python 3.4.5 & 3.5.2 support pathlib.Path.path =
    str(pathlib.Path)
    """
    try:
        relative_path = os.path.relpath(str(path), str(start_at))
    except ValueError:  # when a relative path does not exist
        return get_absolute_path(path)

    return pathlib.Path(relative_path)


def is_file_readable(a_file):
    """
    check if a pathlib.Path() file is readable
    """
    return os.access(str(a_file), os.R_OK)


def is_file_writable(a_file):
    """
    check if a pathlib.Path() file is writable
    """
    return os.access(str(a_file), os.W_OK)


def is_directory_readable(directory):
    """
    check if a pathlib.Path() directory is readable
    """
    return os.access(str(directory), os.R_OK)


def is_directory_writable(directory):
    """
    check if a pathlib.Path() directory is writable
    """
    return os.access(str(directory), os.W_OK)


def is_directory_executable(directory):
    """
    check if a pathlib.Path() directory is executable
    """
    return os.access(str(directory), os.X_OK)

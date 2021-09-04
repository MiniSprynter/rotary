"""
data_tools.py

Module for creating and reading generic data files in various formats.

Lawrence 29/08/21
"""

from pathlib import Path
import pickle


def gen_filepath(filename):
    data_dir = (Path(__file__).parent / "../data").resolve()
    return (data_dir / ("./" + filename + ".pickle")).resolve()


def save(data, filename):
    filepath = gen_filepath(filename)
    with open(filepath, "wb") as data_file:
        pickle.dump(data, data_file)

    return filepath


def load(filename):
    filepath = gen_filepath(filename)
    with open(filepath, "rb") as data_file:
        data = pickle.load(data_file)

    return data

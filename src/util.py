# user define imports
import src.config as config

# python imports
import os
from collections import namedtuple


def get_full_output_path(file_name):
    root_path = os.path.join(".", config.output_path_root)
    full_path = os.path.join(root_path, file_name)
    return full_path


def get_full_log_path(file_name):
    root_path = os.path.join(".", config.log_path_root)
    full_path = os.path.join(root_path, file_name)
    return full_path


def convert_to_const(value):
    Constants = namedtuple('Constants', ['const_value'])
    constants = Constants(value)
    return constants.const_value

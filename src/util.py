#user define imports
import src.config as config

#python imports
import os

def get_full_output_path(file_name):
    root_path = os.path.join(".", config.output_path_root)
    full_path = os.path.join(root_path, file_name)
    return full_path

def get_full_log_path():
    root_path = os.path.join(".", config.log_path_root)
    full_path = os.path.join(root_path, "log.txt")
    return full_path


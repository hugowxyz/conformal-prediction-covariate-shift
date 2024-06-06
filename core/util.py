"""
util.py
"""

import os


def split_all_folders(file_path):
    folders = []
    while True:
        file_path, folder = os.path.split(file_path)
        if folder != "":
            folders.insert(0, folder)
        else:
            if file_path != "":
                folders.insert(0, file_path)
            break
    return folders

"""
Program awareness of path of the program package and folder creation if not available
"""

import os
import pathlib

@staticmethod
def find_folderpath():
    path = str(pathlib.Path().absolute())
    return path

class DirectoryCreator:

    def __init__(self, set_target_directory):
        self.set_target_directory = set_target_directory


    def make_directory(self):
        # check and create new target directory if input given
        if os.path.exists(self):
            print("Path already exists, skip folder creation...")
        else:
            path = os.mkdir(self)
            print("Path " + str(self) + " is created...")
            # read files from target folder "input"
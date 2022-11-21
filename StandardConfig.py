"""
Program awareness of path of the program package and folder creation if not available
"""
import pandas as pd
import glob
import os
import pathlib


class FolderPath:

    @staticmethod
    def find_folderpath():
        path = str(pathlib.Path().absolute())
        return path


class DirectoryCreator:

    def __init__(self, set_target_directory):
        self.set_target_directory = set_target_directory

    def make_directory(self):
        # check and create new target directory if input given
        if os.path.exists(str(self)):
            print("Path already exists, skip folder creation...")
        else:
            path = os.mkdir(str(self))
            print("Path " + str(self) + " is created...")
            # read files from target folder "input"


class TxtLister:

    def __init__(self, path):
        self.path = path

    def txt_lister(self):
        df_name_files = pd.Dataframe(glob.glob(str(self)), sep=";")
        return df_name_files
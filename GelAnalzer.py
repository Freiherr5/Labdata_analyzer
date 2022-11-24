import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage.draw import disk
from skimage.morphology import (erosion, dilation, closing, opening, area_closing, area_opening)
from skimage.color import rgb2gray

class GelVisualizer:

    def __init__(self):
        self


    def gel_plotter(self):
        fig = plt.figure(figsize=(50, 90))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, 60)
        ax.set_ylim(0, 100)
        image = plt.imread('image/' + record.Team + '.png')
        ax.axis("off")
        plt.savefig(str(set_path) + str(set_name) + "_gel.png", dpi=400, bbox_inches="tight")


#Terminal input (2 commands)
#data = sys.argv[1:]
#set_path= data[[1]]
#df_plot = pd.read_fwf(data[[1]])         #plot data for x (time) and y (OD values)
#plot_name = data[[2]]                    #name of the plot and the final file

#optional input for quick testing on my surface (Windows system)
set_path_folder = "C:\\Users\\Feiler Werner\\Desktop\\gel_test_folder\\"
set_file_name = "test_gel"
gel_name = "Testing the Heading"


#Config File input (4 inputs, compare BacGrowth.ini)
config_file = "GelPlot.ini"
config = ConfigParser()
config.read(config_file)
config.sections()


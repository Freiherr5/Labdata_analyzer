import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from configparser import ConfigParser
from PIL import Image

from skimage.io import imread, imshow
from skimage.draw import disk
from skimage.morphology import (erosion, dilation, closing, opening, area_closing, area_opening)
from skimage.color import rgb2gray

class GelVisualizer:

    def __init__(self, path, file, gel_name, marker_df, sample_df, gel_slots, height):
        self.path = path
        self.file = file
        self.gel_name = gel_name
        self.marker_df = marker_df
        self.sample_df = sample_df
        self.gel_slots = gel_slots
        self.height = height


    def gel_plotter(path, gel_slots, file, gel_name, marker_df, sample_df, height):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        img = mpimg.imread(str(path) + str(file)) #the gel image

        i = 0
        while i <= int(gel_slots) -1:
            ax.text(int(sample_df.iloc[i,1]), int(height), sample_df.iloc[i,0], rotation=45, ha = "right", va = "top")
            i = i+1
        ax.set_title(gel_name, fontsize=20)
        ax.axis("off")
        plt.imshow(img)
        plt.savefig(str(path) + str(file) + "_gel.png", dpi=400, bbox_inches="tight")


#Terminal input (2 commands)
#data = sys.argv[1:]
#set_path= data[[1]]
#df_plot = pd.read_fwf(data[[1]])         #plot data for x (time) and y (OD values)
#plot_name = data[[2]]                    #name of the plot and the final file

#optional input for quick testing on my surface (Windows system)
set_path_folder = "C:\\Users\\Feiler Werner\\Desktop\\gel_test_folder\\"
set_file_name = "test_gel.jpg"
gel_name = "Testing the Heading"
marker = "Protein_unstained_marker"


#Config File input (4 inputs, compare BacGrowth.ini)
config_file = "GelAnalyzer.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

factor = float(config["fine_adjustment_of_gel_slots"]["factor"])
x_shift = float(config["fine_adjustment_of_gel_slots"]["x_shift"])

#iterate to get the full table of the marker of choice (marker)
marker_array = []
i = 1
while i <= int(config[str(marker)]["band_amount"]):
    band_name = "band" + str(i)
    band_weight = config[str(marker)][str(band_name)]
    marker_array.append(band_weight)
    i = i+1

#create DataFrame with gel_slot Tag and its position
width, height = Image.open(str(set_path_folder) + str(set_file_name)).size
slot_pixel_width = int(int(width) / int(config["gel_slots"]["gel_slots"]))

sample_array = []
i=0
while i+1 <= int(config["gel_slots"]["gel_slots"]):
    sample_name = "s" + str(i+1)
    sample_tag = config["gel_slots"][sample_name]
    current_pos = (x_shift + slot_pixel_width * (i+1)) * factor
    sample_array.append([sample_tag, current_pos])
    i = i+1
gel_slots = config["gel_slots"]["gel_slots"]
sample_df = pd.DataFrame(sample_array, columns=["slot_name", "x_pos"])

GelVisualizer.gel_plotter(path = set_path_folder, gel_slots= gel_slots, file = set_file_name, gel_name = gel_name, marker_df = marker_array, sample_df = sample_df, height = height)
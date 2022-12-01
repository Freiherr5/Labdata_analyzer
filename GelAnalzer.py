import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from configparser import ConfigParser
from PIL import Image
import MarkerPicker


class GelVisualizer:

    def __init__(self, path, file, gel_name, marker_df, sample_df, gel_slots, height, width):
        self.path = path
        self.file = file
        self.gel_name = gel_name
        self.marker_df = marker_df
        self.sample_df = sample_df
        self.gel_slots = gel_slots
        self.height = height
        self.width = width


    def gel_plotter(path, gel_slots, file, gel_name, marker_df, sample_df, height, width):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        img = mpimg.imread(str(path) + str(file) + ".jpg") #the gel image

        i = 0
        while i <= int(gel_slots) -1:
            ax.text(int(sample_df.iloc[i,1]), int(height), sample_df.iloc[i,0], rotation=45, ha = "right", va = "top", fontsize = 10)
            i = i+1

        i = 0
        while i <= len(marker_df)-1:
            ax.text(int(width*(-0.01)), int(marker_df.iloc[i, 1]), marker_df.iloc[i, 0], ha="right", va="top", fontsize = 7)
            i = i+1

        ax.set_title(gel_name, fontsize=20)
        ax.axis("off")
        plt.imshow(img)
        plt.savefig(str(path) + str(file) + ".png", dpi=400, bbox_inches="tight")


#Terminal input (2 commands)
#data = sys.argv[1:]
#set_path= data[[1]]
#df_plot = pd.read_fwf(data[[1]])         #plot data for x (time) and y (OD values)
#plot_name = data[[2]]                    #name of the plot and the final file

#optional input for quick testing on my surface (Windows system)
set_path_folder = "C:\\Users\\Feiler Werner\\Desktop\\Skerra_data\\SDS_gels\\"
set_file_name = "20221130 2D MBP PDI sec part2"
marker = "Protein_unstained_marker"


#Config File input
config_file = "GelAnalyzer.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

gel_name = config["gel_slots"]["gel_name"]
factor = float(config["fine_adjustment_of_gel_slots"]["factor"])
x_shift = float(config["fine_adjustment_of_gel_slots"]["x_shift"])
x_shift_marker = float(config["fine_adjustment_of_gel_slots"]["x_shift_marker"])


#create DataFrame with gel_slot Tag and its position
width, height = Image.open(str(set_path_folder) + str(set_file_name) + ".jpg").size
slot_pixel_width = int(int(width) / int(config["gel_slots"]["gel_slots"])+1)

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


marker_df = MarkerPicker.get_marker_postion(gel_slots, x_shift_marker, marker = marker, set_file_name = set_file_name, set_path_folder = set_path_folder)


GelVisualizer.gel_plotter(path = set_path_folder, gel_slots = gel_slots, file = set_file_name, gel_name = gel_name, marker_df = marker_df, sample_df = sample_df, height = height, width = width)
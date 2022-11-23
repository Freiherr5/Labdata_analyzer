import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from configparser import ConfigParser
import StandardConfig

class SpectrumPlot:
    def __init__(self, df2, path):
        self.df2 = df2
        self.path = path

    def clean_spectrum(df2, path):
        first_df_name = df2.iloc[0,0]
        initial_df = pd.read_fwf(path + "/" + first_df_name, sep= "\\t", columns=["wavelength", "CD_value", "Voltage"])
        initial_df = initial_df.drop(columns="Voltage")
        i = 1
        while i <= len(df2):
            add_df_name = df2.iloc[i,0]
            add_df = pd.read_fwf(path + "/" + add_df_name, sep="\\t", columns=["wavelength", "CD_value", "Voltage"])
            add_df = add_df.drop(columns="Voltage")
            initial_df.join(add_df)
            i = i+1

        # clean DataFrame from junk data on top and bottom of the table
        droptop_df = initial_df.drop(initial_df.index[0:12])
        dropbottom_df = droptop_df.drop()





    def spectrum_plot(self, set_name, set_directory, set_color):
        df_CD_min = np.array(self.idxmin())
        min_CD_value = self.iloc[df_CD_min[1], 1]
        wavelength_min = self.iloc[df_CD_min[1], 0]

        plt.figure(figsize=(10, 10))
        ax2 = plt.subplot(1, 1, 1)

        ax2.scatter(data=self, x="Wavelength", y="CD_value", color=str(set_color))
        ax2.set_ylabel("$deg$ $cm^{2}$ $dmol^{-1}$", fontsize=15)
        ax2.set_xlabel("wavelength [nm]", fontsize=15)
        x1, y1 = (wavelength_min, wavelength_min), (min_CD_value - 5, min_CD_value)
        x2, y2 = (190, wavelength_min), (min_CD_value, min_CD_value)
        plt.plot(x1, y1, color="black", linestyle="--")
        plt.plot(x2, y2, color="black", linestyle="--")
        plt.scatter(wavelength_min, min_CD_value, color="black")
        ax2.text(wavelength_min + 5, min_CD_value - 5, "$CD_{min}$ = " + str(wavelength_min) + " nm", fontsize=15)
        ax2.set_title("Spektrum " + str(set_name), fontsize=25)

        plt.savefig(str(set_directory) + str(set_name) + "_spectrum.png", dpi=400, bbox_inches="tight")





#Terminal input (2 commands)
data = sys.argv[1:]
set_path_folder = data[[0]]               #the idea is to generate up to 3 graphs in one figure if a comparison is needed
plot_name = data[[1]]                    #name of the plot and the final file


#Config File input (5 inputs, compare CD.ini)
config_file = "CD.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

graph_color1 = config["CD_spec"]["graph_color1"]
graph_color2 = config["CD_spec"]["graph_color2"]
graph_color3 = config["CD_spec"]["graph_color3"]
start_range = config["CD_spec"]["start_range"]
max_range = config["CD_spec"]["max_range"]


txt_name_df = StandardConfig.TxtLister.txt_lister(set_path_folder) # returns dataframe with names of txt files


cleaned_df = SpectrumPlot.clean_spectrum(txt_name_df, set_path_folder) #first function of the program
SpectrumPlot.spectrum_plot()

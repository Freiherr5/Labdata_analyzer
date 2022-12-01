import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from configparser import ConfigParser
import StandardConfig

class SpectrumPlot:
    def __init__(self, df2, path, name, tags, graph_name, start_range, max_range):
        self.df2 = df2
        self.path = path
        self.name = name
        self.tags = tags
        self.graph_name = graph_name
        self.start_range = start_range
        self.max_range = max_range

    def clean_spectrum(df, path):

        #make dataframe with one to multiple spectra plotted in one figure for comparison
        first_df_name = df.iloc[0,0]
        initial_df = pd.read_fwf(path + "/" + first_df_name, sep= "\\t", columns=["Wavelength0", "CD_value0", "Voltage"])
        initial_df = initial_df.drop(columns="Voltage")
        i = 1
        while i <= len(df):
            add_df_name = df.iloc[i,0]
            add_df = pd.read_fwf(path + "/" + add_df_name, sep="\\t", columns=["Wavelength" + str(i), "CD_value" + str(i), "Voltage"])
            add_df = add_df.drop(columns="Voltage")
            initial_df.join(add_df)
            i = i+1

        # clean DataFrame from junk data on top and bottom of the table
        droptop_df = initial_df.drop(initial_df.index[0:12])
        end_index = list(np.where(droptop_df["wavelength"] == "##### Extended Information")[0])
        dropbottom_df = droptop_df.drop(droptop_df.index[end_index:])
        return dropbottom_df

    def spectrum_plot(df, tags, path, graph_name, start_range, max_range):

        plt.figure(figsize=(10, 10))
        ax = plt.subplot(1, 1, 1)
        plt.xlim([int(start_range), int(max_range)])
        # iterated unit to have multiple graphs in one figure

        i = 0
        while i <= len(subgraphs_df):
            #for each iteration determine the global CD minimum in dependancy to the wavelength
            sliced_df = df[["Wavelength" + str(i),"CD_value" + str(i)]].copy()
            df_CD_min = np.array(sliced_df.idxmin())
            min_CD_value = df_CD_min.iloc[df_CD_min[1], 1]
            wavelength_min = df_CD_min.iloc[df_CD_min[1], 0]

            #graph plotting
            ax.scatter(data=sliced_df, x="Wavelength" + str(i), y="CD_value" + str(i), color=str(tags.iloc[1, i]), label=str(tags.iloc[0, i]))

            #defines the global CD value minimum
            x1, y1 = (wavelength_min, wavelength_min), (min_CD_value - 5, min_CD_value)
            x2, y2 = (190, wavelength_min), (min_CD_value, min_CD_value)
            plt.plot(x1, y1, color="black", linestyle="--")
            plt.plot(x2, y2, color="black", linestyle="--")
            plt.scatter(wavelength_min, min_CD_value, color="black")
            ax.text(wavelength_min + 5, min_CD_value - 5, "$CD_{min}$ = " + str(wavelength_min) + " nm", fontsize=15)

            i = i+1

        ax.set_title("Spektrum " + str(graph_name), fontsize=25)
        ax.set_ylabel("$deg$ $cm^{2}$ $dmol^{-1}$", fontsize=15)
        ax.set_xlabel("wavelength [nm]", fontsize=15)

        plt.legend()

        plt.savefig(str(path) + str(graph_name) + "_spectrum.png", dpi=400, bbox_inches="tight")





#Terminal input (3 main input types), iteration over name_legend (individual graph name) and its color, since many graphs can be generated

data = sys.argv[1:]
set_path_folder = data[[1]]
i = 0
array_subgraphs = []
while i <= len(data)-2:
    name_legend = data[[2 + (2*i)]]
    color = data[[3 + (2*i)]]
    array_subgraphs.append([name_legend, color])
    i = i+1
subgraphs_df = pd.DataFrame(array_subgraphs, columns=["name_legend", "color"])   #outputs dataframe with all the information for each individual graph (sys.argv)


#Config File input (5 inputs, compare CD.ini)
config_file = "CD.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

graph_name = config["CD_spec"]["graph_name"]             #heading and file name of plotted .png
start_range = config["CD_spec"]["start_range"]
max_range = config["CD_spec"]["max_range"]


txt_name_df = StandardConfig.TxtLister.txt_lister(set_path_folder) # returns dataframe with names of txt files
cleaned_df = SpectrumPlot.clean_spectrum(df=txt_name_df, path=set_path_folder) #returns one dataframe with all graphs (alternating wavelength and CD value)
SpectrumPlot.spectrum_plot(df=cleaned_df, tags= subgraphs_df, path = set_path_folder, graph_name = graph_name, start_range = start_range, max_range = max_range)

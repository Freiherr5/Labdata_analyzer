import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from configparser import ConfigParser

class HeatPlot:

    def __init__(self, df):
        self.df = df

    def normalize_heat(self):
        pass

    def plot_heat(self, set_show=1, set_name="CD_heat", set_directory=str(path) + "/output_graphs/", set_color="r"):

        # plotting of the graph (singular, not multiple graphs in one figure)
        plt.figure(figsize=(10, 10))
        ax1 = plt.subplot(1, 1, 1)
        plt.xlim([]) #insert start_temp and max_temp


        ax1.scatter(data=self, x="temperature", y="norm_heat", color=str(set_color))
        ax1.text(temp50 - 25, 0, "$T_{1/2}$ = " + str(temp50) + " °C", fontsize=15)
        ax1.set_title("Heat denaturation of " + str(set_name), fontsize=25)
        x1, y1 = (temp50, temp50), (0.5, 0)  # first bracket is for the x values, second for the y brackets
        x2, y2 = (20, temp50), (0.5, 0.5)
        plt.plot(x1, y1, color="black", linestyle="--")
        plt.plot(x2, y2, color="black", linestyle="--")
        plt.scatter(temp50, 0.5, color="black")

        ax1.set_xlabel("temperature [°C]", fontsize=15)
        ax1.set_ylabel("relative protein nativity", fontsize=15)
        ax1.set_title("Heat denaturation of " + str(set_name), fontsize=25)
        ax1.text(temp50 - 25, 0, "$T_{1/2}$ = " + str(temp50) + " °C", fontsize=15)
        ax1.set_title("Heat denaturation of " + str(set_name), fontsize=25)
        plt.legend()

        plt.xticks(np.arange(20, max_temp + 1, 10))
        plt.yticks(np.arange(0, 1 + 0.1, 0.1))




        plt.savefig(str(set_directory) + str(set_name) + "_heat.png", dpi=400, bbox_inch= "tight")


#Terminal input (3 main input types), iteration over name_legend (individual graph name) and its color, since many graphs can be generated

data = sys.argv[1:]
set_path_folder = data[[1]]
i = 0
array_subgraphs = []
while i <= len(data) -2:
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

graph_name = config["CD_heat"]["graph_name"]
start_temp = config["CD_heat"]["start_temp"]
max_temp = config["CD_heat"]["max_temp"]
linear_regression_range = config["CD_heat"]["linear_regression_range"]
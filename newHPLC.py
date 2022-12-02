import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser
import sys
import StandardConfig

class HPLC:

    def __init__(self):


    def sec_norm(path, name_excel):
        # clean dataframe for plotting

        df = pd.read_excel(str(path) + str(name_excel))
        df = df[["10", "Unnamed 1"]]
        df = df.drop(df.index[0:2])
        df = df.rename(columns = {"10" : "volume0", "Unnamed 1" : "UV0"})

        # join all dataframes with relevant values

        i = 1
        while i <= len(name_excel):
            df_inter = pd.read_excel(str(path) + str(name_excel))
            df_inter = df_inter[["10", "Unnamed 1"]]
            df_inter = df_inter.drop(df.index[0:2])
            df_inter = df.rename(columns={"10": "volume" + str(i), "Unnamed 1": "UV" + str(i)})
            df.join(df_inter)
            i = i + 1

        # extract local maxima from dataframe






    def hplc_plot(self, df_frac, set_name, set_directory, set_color):
        plt.figure(figsize=(25, 10))
        ax1 = plt.subplot(1, 1, 1)

        ax2 = ax1.twinx()
        l1 = ax1.scatter(data=self, x="Volume", y="UV/Vis signal", color=str(set_color), label="UV/Vis signal")

        ax1.set_ylabel("UV/Vis signal [mAU]", fontsize=15)
        ax1.set_xlabel("Volume [ml]", fontsize=15)
        ax1.set_title("Chromatogram of " + str(set_name), fontsize=25)
        plt.scatter(x=0, y=-20, color="white")
        l2 = ax2.scatter(data=self, x="Volume", y="Conductivity", color="black", label="Conductivity")
        ax2.set_ylabel("Conductivity [mS/cm]", fontsize=15)
        labels = [l1, l2]
        labs = [l.get_label() for l in labels]
        plt.legend(labels, labs, loc=0)
        AlignPlot.align_yaxis(ax1, 0, ax2, 0)
        # generation of fraction markings if given --> != 0
        if df_frac.iloc[0, 0] != "nothing":
            plt.text(0.0, -20.0, "Fractions:", fontsize=15)
            p = 0
            while p <= (len(df_frac.index) - 1):
                plt.text(float(df_frac.iloc[p, 0]), -20.0, df_frac.iloc[p, 1])
                p = p + 1


            plt.savefig(str(set_directory) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")



















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

txt_name_df = StandardConfig.TxtLister.txt_lister(set_path_folder) # returns dataframe with names of txt files

HPLC.sec_norm(path=set_path_folder, name_excel=txt_name_df)
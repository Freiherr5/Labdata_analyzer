import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import AlignPlot
import sys
from configparser import ConfigParser

# pathlib and mkdir
import StandardConfig


class HPLC:

    def __init__(self, df3):
        self.df3 = df3

    def clean_graph(self):
        # primary table for UV signal volume graph
        sum_array_hplc = []
        i = 2
        while i != int(len(self.df3.index)):
            intermediate0_hplc = str(self.df3.iloc[i, 0]).split("\t")[0]
            intermediate1_hplc = str(self.df3.iloc[i, 0]).split("\t")[1]
            intermediate2_hplc = str(self.df3.iloc[i, 0]).split("\t")[3]
            sum_array_hplc.append([intermediate0_hplc, intermediate1_hplc, intermediate2_hplc])
            i = i + 1
        df_hplc_clean = pd.DataFrame(sum_array_hplc, dtype=np.float64,
                                     columns=["Volume", "UV/Vis signal", "Conductivity"])

        if df_hplc_clean.Volume[df_hplc_clean.Volume > 30.0].any() == True:
            new_cutoff = df_hplc_clean.Volume[df_hplc_clean.Volume > 30.0].min()
            inter = df_hplc_clean["Volume"].where(df_hplc_clean["Volume"] == new_cutoff).dropna(axis="rows").index[0]
            df_inter_hplc_clean = df_hplc_clean.truncate(0, inter, axis="rows")
            df_hplc_clean = df_inter_hplc_clean
            return df_hplc_clean
        else:
            return df_hplc_clean

    def clean_frac(self, txt_name="unnamed"):
        pass

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


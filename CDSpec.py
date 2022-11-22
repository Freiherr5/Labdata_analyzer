import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from configparser import ConfigParser

# pathlib and mkdir
import StandardConfig


class SpectrumPlot:
    def __init__(self, df2):
        self.df2 = df2

    def clean_spectrum(self):
        pass
    def spectrum_plot(self, set_show=1, set_name="protein", set_directory=str(path) + "/output_graphs/", set_color="r"):
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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from configparser import ConfigParser

# pathlib and mkdir
import StandardConfig


class HeatPlot:
    # set base path independant of device:
    path = str(pathlib.Path().absolute())  # /home/user/Analyzer_Hagn_Data_package

    @staticmethod
    def help():
        print("""
          Functions of the script: 

          normalize_heat(df = fwf one column dataframe with \\t separation)
            --> returns normalized CD values in correlation to the temperature (DataFrame)

          plot_heat --> dataframe from the prior normalize_heat method

          """)

    def __init__(self, df):
        self.df = df

    def normalize_heat(self):
        pass

    def plot_heat(self, set_show=1, set_name="CD_heat", set_directory=str(path) + "/output_graphs/", set_color="r"):

        # generating temp50; searches the temperature where 50% of the protein is denaturated
        df_50 = self.loc[(self["norm_heat"] >= 0.40) & (self["norm_heat"] <= 0.60)]

        # taking just the mean is to inaccurate
        """
        df_50_mean = df_50.mean()
        df_50_result_temp = (df_50_mean.iloc[1] * df_50_mean.iloc[0]) / 0.5
        temp50 = round(df_50_result_temp, 2)
        """

        # Linear regression is necessary to boost accuracy of the 50% protein denaturation value
        # mean x and y
        df_50_mean = df_50.mean()
        xmean = df_50_mean.iloc[0]
        ymean = df_50_mean.iloc[1]

        # covariance and variance
        array_var = []
        v = 0
        while v <= len(df_50) - 1:
            xycov = (df_50.iloc[v, 0] - xmean) * (df_50.iloc[v, 1] - ymean)
            xvar = (df_50.iloc[v, 0] - xmean) ** 2
            array_inter = [xycov, xvar]
            array_var.append(array_inter)
            v = v + 1
        df_var = pd.DataFrame(array_var, columns=["xycov", "xvar"])

        # alpha and beta for the term: Y = a + b*X
        xycov_sum = round(df_var.sum(axis=0)[0], 2)
        xvar_sum = round(df_var.sum(axis=0)[1], 2)
        beta = (xycov_sum / xvar_sum)
        alpha = ymean - (beta * xmean)
        temp50_pre = (0.5 - float(alpha)) / float(beta)
        temp50 = round(temp50_pre, 2)

        # plotting of the graph (singular, not multiple graphs in one figure)
        max_temp = 110
        plt.figure(figsize=(10, 10))
        ax1 = plt.subplot(1, 1, 1)
        ax1.scatter(data=self, x="temperature", y="norm_heat", color=str(set_color))
        ax1.set_xlabel("temperature [°C]", fontsize=15)
        ax1.set_ylabel("relative protein nativity", fontsize=15)
        x1, y1 = (temp50, temp50), (0.5, 0)  # first bracket is for the x values, second for the y brackets
        x2, y2 = (20, temp50), (0.5, 0.5)
        plt.plot(x1, y1, color="black", linestyle="--")
        plt.plot(x2, y2, color="black", linestyle="--")
        plt.scatter(temp50, 0.5, color="black")
        ax1.text(temp50 - 25, 0, "$T_{1/2}$ = " + str(temp50) + " °C", fontsize=15)
        ax1.set_title("Heat denaturation of " + str(set_name), fontsize=25)
        plt.xticks(np.arange(20, max_temp + 1, 10))
        plt.yticks(np.arange(0, 1 + 0.1, 0.1))

        if set_show != 0:
            plt.show()
        else:
            plt.savefig(str(set_directory) + str(set_name) + "_heat.png", dpi=400, bbox_inch= "tight")
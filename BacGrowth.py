import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys
from configparser import ConfigParser

# pathlib and mkdir
import StandardConfig


class GrowthObserver:

    def __init__(self, df):
        self.df = df

    path = StandardConfig.find_folderpath()    #path of the folder with the scripts
    def plot_growth(self, set_name="bacteria_plot", set_color="red", set_directory=path + "/output/", set_time_scale = "min", induction_point ="0", set_inducer = "IPTG", set_OD = "600"):
        plt.figure(figsize=(15, 10))
        ax1 = plt.subplot(1, 1, 1)
        ax1.scatter(self, x="Time [" + set_time_scale + "]", y="$OD_" + set_OD + "$", color=str(set_color))
        ax1.set_ylabel("$OD_600$", fontsize=15)
        ax1.set_xlabel("Volume [ml]", fontsize=15)
        ax1.set_title("Growth of " + str(set_name), fontsize=25)

        #create line with the marking of point of induction and inducer
        x_induction = self[int(induction_point), 0]
        y_induction = self[int(induction_point), 1]


        x1, y1 = [x_induction, x_induction], [-0.5, y_induction] # requires two points for line --> nametag point and graph point
        plt.plot(x1, y1, color="black")
        plt.text(float(x_induction), - 0.5, set_inducer)  #name induction agent for protein production



        x = []                  #Interpolation of scatter points
        y = []

        for i in self:
            x_append = self.iloc[i, 0]
            y_append = self.iloc[i, 1]
            x.append(x_append)
            y.append(y_append)

        # x_new, bspline, y_new
        x_new = np.linspace(1, 5, 50)
        bspline = interpolate.make_interp_spline(x, y)
        y_new = bspline(x_new)

        # Plot the new data points
        plt.plot(x_new, y_new)

        plt.savefig(str(set_directory) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")

#Terminal input (2 commands)
data = sys.argv[1:]
array_plot = data[[0]]                   #plot data for x and y
df_plot = pd.DataFrame(array_plot)
plot_name = data[[1]]                    #name of the plot and the final file

#Config File input (3 inputs, compare BacGrowth.ini)
config_file = "BacGrowth.ini"
config = ConfigParser()
config.read(config_file)
config.sections()
df_config = pd.DataFrame(list(config["growth_bacteria_pLot"]))
set_path = df_config.iloc[0,0]
graph_color = df_config.iloc[1,0]        #color of graph
time_scale = df_config[2,0]              #hours or minutes
induction_point = df_config[3,0]         #when was the Inducer added
set_inducer = df_config[4,0]             #sets the name of the induction agent
set_OD = df_config[5,0]                  #set the wavelength used for the OD measurement


GrowthObserver.plot_growth(array_plot, set_name=plot_name, set_color=graph_color, set_time_scale = time_scale, induction_point = induction_point, set_inducer= set_inducer, set_OD = set_OD)
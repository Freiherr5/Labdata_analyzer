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

    path = StandardConfig.FolderPath.find_folderpath()    #path of the folder with the scripts
    def plot_growth(self, set_name="bacteria_plot", set_color="red", set_path =path + "/output/", induction_point ="0", set_inducer = "IPTG", set_OD = "600"):
        df_column = self.columns[0]
        plt.figure(figsize=(15, 10))
        ax1 = plt.subplot(1, 1, 1)
        ax1.scatter(data=self, x=df_column, y="OD", color=str(set_color))
        ax1.set_ylabel("$OD_" + set_OD + "$", fontsize=15)
        ax1.set_xlabel("Time [" + df_column + "]", fontsize=15)
        ax1.set_title("Growth of " + str(set_name), fontsize=25)

        #create line with the marking of point of induction and inducer
        x_induction = self.iloc[int(induction_point), 0]
        y_induction = self.iloc[int(induction_point), 1]


        x1, y1 = [x_induction, x_induction], [-0.5, y_induction] # requires two points for line --> nametag point and graph point
        plt.plot(x1, y1, color="black")
        plt.text(float(x_induction), - 0.5, set_inducer)  #name induction agent for protein production



        x = []                  #Interpolation of scatter points
        y = []

        i=0
        while i <= len(self)-1:
            x_append = self.iloc[i, 0]
            y_append = self.iloc[i, 1]
            x.append(x_append)
            y.append(y_append)
            i = i+1

        # x_new, bspline, y_new
        x_new = np.linspace(1, 5, 50)
        bspline = interpolate.make_interp_spline(x, y)
        y_new = bspline(x_new)

        # Plot the new data points
        plt.plot(x_new, y_new)

        plt.savefig(str(set_path) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")





#Terminal input (2 commands)
# data = sys.argv[1:]
# array_plot = data[[0]]                   #plot data for x (time) and y (OD values)
# df_plot = pd.DataFrame(array_plot)
# plot_name = data[[1]]                    #name of the plot and the final file

#optional input for quick testing
df_plot = pd.read_fwf("/home/Freiherr/PycharmProjects/Labdata_analyzer/Test_BacGrowth/bac_growth.txt", index = "h")
plot_name = "Origami B pASK75 MBP - LepR 2D"


#Config File input (3 inputs, compare BacGrowth.ini)
config_file = "BacGrowth.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

set_path = config["growth_bacteria_pLot"]["path"]
graph_color = config["growth_bacteria_pLot"]["graph_color"]      #color of graph
induction_point = config["growth_bacteria_pLot"]["induction_point"]       #when was the Inducer added
set_inducer = config["growth_bacteria_pLot"]["inducer"]           #sets the name of the induction agent
set_OD = config["growth_bacteria_pLot"]["set_OD"]                #set the wavelength used for the OD measurement


GrowthObserver.plot_growth(df_plot, set_name = plot_name, set_color = graph_color, set_path = set_path, induction_point = induction_point, set_inducer= set_inducer, set_OD = set_OD)
#/home/Freiherr/PycharmProjects/Labdata_analyzer/
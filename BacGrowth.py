import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from configparser import ConfigParser
import sys


class GrowthObserver:

    def __init__(self, df, set_name, set_color, set_path, induction_point, set_inducer, set_OD):
        self.df = df
        self.set_name = set_name
        self.set_color = set_color
        self.set_path = set_path
        self.induction_point = induction_point
        self. set_inducer = set_inducer
        self.set_OD = set_OD

    def plot_growth(df, set_name, set_color, set_path, induction_point, set_inducer, set_OD):
        df_column = df.columns[0]
        plt.figure(figsize=(15, 10))
        ax1 = plt.subplot(1, 1, 1)
        ax1.scatter(data=df, x=df_column, y="OD", color=str(set_color))
        ylabel = "$OD_{" + str(set_OD) + "}$"
        ax1.set_ylabel(ylabel, fontsize=20)
        ax1.set_xlabel("$Time [" + df_column + "]$", fontsize=20)
        ax1.set_title("Growth of " + str(set_name), fontsize=30)

        #create line with the marking of point of induction and inducer
        x_induction = df.iloc[int(induction_point), 0]
        y_induction = df.iloc[int(induction_point), 1]


        x1, y1 = [x_induction, x_induction], [0, y_induction] # requires two points for line --> nametag point and graph point
        plt.plot(x1, y1, color="black")
        plt.text((float(x_induction) + 0.2), 0, set_inducer, fontsize=20)  #name induction agent for protein production

        #Transform dataframe in 2 arrays for x (time) and y (OD)
        x = df[df_column].to_numpy()
        y = df["OD"].to_numpy()

        #create new x and y values for polynome fit

        poly = np.polyfit(x, y, deg = 4)
        plt.plot(np.polyval(poly, x), "--", color = set_color)

        plt.savefig(str(set_path) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")





#Terminal input (2 commands)
#data = sys.argv[1:]
#set_path_folder = data[[0]]
#set_file_name = data[[1]]
#df_plot = pd.read_fwf(data[[1]])         #plot data for x (time) and y (OD values)
#plot_name = data[[2]]                    #name of the plot and the final file

#optional input for quick testing on my surface (Windows system)
set_path_folder = "C:\\Users\\Feiler Werner\\Desktop\\Skerra_data\\20221123_2D3Dgrow\\"
set_file_name = "3D.txt"
df_plot = pd.read_fwf(set_path_folder + set_file_name, index = "h")
plot_name = "Origami B pASK75 MBP-LepR3D-PDI"


#Config File input (4 inputs, compare BacGrowth.ini)
config_file = "BacGrowth.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

graph_color = config["growth_bacteria_pLot"]["graph_color"]               #color of graph
induction_point = config["growth_bacteria_pLot"]["induction_point"]       #when was the Inducer added
set_inducer = config["growth_bacteria_pLot"]["inducer"]                   #sets the name of the induction agent
set_OD = config["growth_bacteria_pLot"]["set_OD"]                         #set the wavelength used for the OD measurement


GrowthObserver.plot_growth(df_plot, set_name = plot_name, set_color = graph_color, set_path = set_path_folder, induction_point = induction_point, set_inducer= set_inducer, set_OD = set_OD)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from configparser import ConfigParser




class GrowthObserver:

    def __init__(self, df):
        self.df = df


    def plot_growth(self, set_name, set_color, set_path, induction_point, set_inducer, set_OD):
        df_column = self.columns[0]
        plt.figure(figsize=(15, 10))
        ax1 = plt.subplot(1, 1, 1)
        ax1.scatter(data=self, x=df_column, y="OD", color=str(set_color))
        ylabel = "$OD_{" + str(set_OD) + "}$"
        ax1.set_ylabel(ylabel, fontsize=15)
        ax1.set_xlabel("Time [" + df_column + "]", fontsize=15)
        ax1.set_title("Growth of " + str(set_name), fontsize=25, fontweight ="semibold")

        #create line with the marking of point of induction and inducer
        x_induction = self.iloc[int(induction_point), 0]
        y_induction = self.iloc[int(induction_point), 1]


        x1, y1 = [x_induction, x_induction], [-0.5, y_induction] # requires two points for line --> nametag point and graph point
        plt.plot(x1, y1, color="black")
        plt.text(float(x_induction), -1, set_inducer, fontsize=15)  #name induction agent for protein production

        #Transform dataframe in 2 arrays for x (time) and y (OD)
        x = self[df_column].to_numpy()
        y = self["OD"].to_numpy()

        #create new x and y values for interpolation graph
        y_new = interp1d(x, y, kind="cubic")
        x_new = np.linspace(x[0], x[-1], num=100, enpoint=True) #first two values set the range --> needs to be extracted from x

        # Plot the new data points
        plt.plot(x_new, y_new, "-")

        plt.savefig(str(set_path) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")





#Terminal input (2 commands)
# data = sys.argv[1:]
# df_plot = pd.read_fwf(data[[0]])         #plot data for x (time) and y (OD values)
# plot_name = data[[1]]                    #name of the plot and the final file

#optional input for quick testing
df_plot = pd.read_fwf("/home/Freiherr/PycharmProjects/Labdata_analyzer/Test_BacGrowth/bac_growth.txt", index = "h")
plot_name = "Origami B pASK75 MBP - LepR 2D"


#Config File input (3 inputs, compare BacGrowth.ini)
config_file = "BacGrowth.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

set_path = config["growth_bacteria_pLot"]["path"]                         #path of target folder to save the graph
graph_color = config["growth_bacteria_pLot"]["graph_color"]               #color of graph
induction_point = config["growth_bacteria_pLot"]["induction_point"]       #when was the Inducer added
set_inducer = config["growth_bacteria_pLot"]["inducer"]                   #sets the name of the induction agent
set_OD = config["growth_bacteria_pLot"]["set_OD"]                         #set the wavelength used for the OD measurement


GrowthObserver.plot_growth(df_plot, set_name = plot_name, set_color = graph_color, set_path = set_path, induction_point = induction_point, set_inducer= set_inducer, set_OD = set_OD)
#/home/Freiherr/PycharmProjects/Labdata_analyzer/
import pandas as pd
import numpy as np
import AlignPlot
import matplotlib.pyplot as plt
from configparser import ConfigParser
import math
import sys
import StandardConfig
from scipy.signal import argrelextrema

class HPLC:

    def __init__(self, path, name_excel, df, a, b, V0, V_total, V_elu_array):
        self.path = path
        self.name_excel = name_excel
        self.df = df  #cleaned df
        self.a = a   #factor of log(MW)
        self.b = b   #variable of Kav
        self.V0 = V0
        self.V_total = V_total
        self.V_elu_array = V_elu_array   #smart recognition of local maxima of the chromatogram


    def peak_picker(df):
        fit = np.polyfit(df["ml_mAU"], df["mAU"], 10)
        pf = np.poly1d(fit)
        pf_array_index = argrelextrema(pf, np.greater, mode="wrap")[0]
        return pf_array_index
    def calculate_MW(a, b, V0, V_total, V_elu_array):
        # base formula = Kav = a * log(MW) + b     --->     transform to calculate MW

        i = 0
        array_ml_MW = []

        while i <= len(V_elu_array):
            MW_i = math.pow(10, (((V_elu_array[i]-V0)/(V_total-V0)-b)/a))
            array_ml_MW.append(i, MW_i)
            i = i + 1

        df_ml_MW = pd.DataFrame(array_ml_MW, columns=["ml", "MW"])
        return df_ml_MW


    def sec_norm(path, name_excel):
        # clean dataframe for plotting

        df_all = pd.read_excel(str(path) + str(name_excel), header = 2)
        array_columns = list(df_all.columns)    #creates array with all column names, search for "mAU" and optional "mS/cm", "(Injections)" = Fractions

        #find positions of the columns of interest and get both columns: volume [ml] (on the left side of the column of interest)

        array_of_interest = []

        # dataframe part that is always present:
        ml = array_columns[0]
        mAU = array_columns[1]
        df_mAU = df_all.copy(df_all.columns[0, 1])
        array_of_interest.append(df_mAU.rename(columns={ml : "ml_mAU", mAU : "mAU"}))

        if "mS/cm" in array_columns is True:
            index_mS = array_columns.index("mS/cm")
            ml = array_columns[index_mS-1]
            mS = array_columns[index_mS]
            df_mS = df_all.copy(df_all.columns[ml, mS])
            array_of_interest.append(df_mS.rename(columns={ml : "ml_mS", mS : "mS"}))

        if "(Injections)" in array_columns is True:
            index_In = array_columns.index("(Injections)")
            ml = array_columns[index_In - 1]
            In = array_columns[index_In]
            df_mS = df_all.copy(df_all.columns[ml, In]).dropna()
            array_of_interest.append(df_mS.rename(columns={ml: "ml_In", In: "Fractions"}))

        return array_of_interest


    def hplc_plot(array, set_name, set_directory, set_color):
        df_mAU = array[0]
        if len(array)  == 2:
            df_2 = array[1]
        if len(array) == 3:
            df_3 = array[2]


        plt.figure(figsize=(25, 10))
        ax1 = plt.subplot(1, 1, 1)

        ax2 = ax1.twinx()
        l1 = ax1.scatter(data=df_mAU, x="ml_mAU", y="mAU", color=str(set_color), label="UV/Vis signal")

        ax1.set_ylabel("UV/Vis signal [mAU]", fontsize=15)
        ax1.set_xlabel("Volume [ml]", fontsize=15)
        ax1.set_title("Chromatogram of " + str(set_name), fontsize=25)
        plt.scatter(x=0, y=-20, color="white")

        if "mS/cm" in list(df_2.columns) is True:
            l2 = ax2.scatter(data=df_2, x="Volume", y="Conductivity", color="black", label="Conductivity")
            ax2.set_ylabel("Conductivity [mS/cm]", fontsize=15)
            labels = [l1, l2]
            labs = [l.get_label() for l in labels]
            plt.legend(labels, labs, loc=0)
            AlignPlot.align_yaxis(ax1, 0, ax2, 0)

        if "(Injections)" in list(df_3.columns) is True:
            plt.text(0.0, -20.0, "Fractions:", fontsize=15)
            p = 0
            while p <= (len(df_3.index) - 1):
                plt.text(float(df_3.iloc[p, 0]), -20.0, df_3.iloc[p, 1])
                p = p + 1

        plt.savefig(str(set_directory) + str(set_name) + "_hplc.png", dpi=400, bbox_inches="tight")




#Terminal input (3 commands)
#data = sys.argv[1:]
#set_path= data[[0]]
#df_plot = pd.read_fwf(data[[1]])         #plot data for x (time) and y (OD values)
#plot_name = data[[2]]                    #name of the plot and the final file



HPLC.sec_norm(path=set_path_folder, name_excel=txt_name_df)
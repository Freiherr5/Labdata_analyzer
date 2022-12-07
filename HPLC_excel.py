import pandas as pd
import numpy as np
import AlignPlot
import matplotlib.pyplot as plt
from configparser import ConfigParser
import math
import sys
from scipy import signal


class HPLC:

    def __init__(self, path, name_excel, name, df, a, b, V0, V_total, V_elu_df, array, array_df, color):
        self.color = color
        self.name = name      # name of the plot + Heading
        self.array = array    # array with local/global maxima
        self.array_df = array_df
        self.path = path
        self.name_excel = name_excel
        self.df = df  #cleaned df
        self.a = a   #factor of log(MW)
        self.b = b   #variable of Kav
        self.V0 = V0
        self.V_total = V_total
        self.V_elu_df = V_elu_df   #smart recognition of local maxima of the chromatogram (packaged as DataFrame)


    def peak_picker(df):

        # use scipy find_peaks
        array_mAU = df["mAU"].to_numpy()
        peaks = pd.DataFrame(signal.find_peaks(array_mAU, prominence = 0.2)).transpose()[0]
        return peaks

    def calculate_MW(a, b, V0, V_total, V_elu_df, df):
        # base formula = Kav = a * log(MW) + b     --->     transform to calculate MW

        i = 0
        array_ml_MW = []

        while i <= len(V_elu_df)-1:
            MW_i = round(math.pow(10, ((((float(df.iloc[int(V_elu_df.values[i]), 0])-V0)/(V_total-V0))-b)/a)), 1)
            ml_i = float(df.iloc[int(V_elu_df.values[i]), 0])
            UV_Vis_signal = float(df.iloc[int(V_elu_df.values[i]), 1]) + float(df.iloc[int(V_elu_df.values[0]), 1])*0.05
            array_ml_MW.append([ml_i, UV_Vis_signal, MW_i])
            i = i + 1

        df_ml_MW = pd.DataFrame(array_ml_MW, columns=["ml", "UV/Vis", "MW"])
        return df_ml_MW


    def sec_norm(path, name_excel):
        # clean dataframe for plotting

        df_all = pd.read_excel(str(path) + str(name_excel) + ".xls", header = 2)
        array_columns = list(df_all.columns)    #creates array with all column names, search for "mAU" and optional "mS/cm", "(Injections)" = Fractions

        #find positions of the columns of interest and get both columns: volume [ml] (on the left side of the column of interest)

        array_of_interest = []

        # dataframe part that is always present:
        ml = array_columns[0]
        mAU = array_columns[1]
        df_mAU = df_all[[ml, mAU]].copy()
        array_of_interest.append(df_mAU.rename(columns={ml : "ml_mAU", mAU : "mAU"}))

        if "mS/cm" in array_columns:
            index_mS = array_columns.index("mS/cm")
            ml = array_columns[index_mS-1]
            mS = array_columns[index_mS]
            df_mS = df_all[[ml, mS]].copy()
            array_of_interest.append(df_mS.rename(columns={ml : "ml_mS", mS : "mS"}))

        if "(Fractions)" in array_columns:
            index_In = array_columns.index("(Fractions)")
            ml = array_columns[index_In - 1]
            In = array_columns[index_In]
            df_In = df_all[[ml, In]].copy().dropna()
            array_of_interest.append(df_In.rename(columns={ml: "ml_In", In: "Fractions"}))

        return array_of_interest


    def hplc_plot(array_df, df, name, path, color):
        df_mAU = array_df[0]
        df_2 = ["-"]
        df_3 = ["-"]

        if len(array_df) == 2:
            df_2 = array_df[1]

        if len(array_df) == 3:
            df_3 = array_df[2]

        if list(df_2.columns)[1] == "Fractions":
            df_3 = df_2

        plt.figure(figsize=(25, 10))
        ax1 = plt.subplot(1, 1, 1)

        # if Conductivity column was present and wanted
        if "mS/cm" in list(df_2.columns):
            ax2 = ax1.twinx()

        l1 = ax1.scatter(data=df_mAU, x="ml_mAU", y="mAU", color=str(color), label="UV/Vis signal")

        ax1.set_ylabel("UV/Vis signal [mAU]", fontsize=15)
        ax1.set_xlabel("Volume [ml]", fontsize=15)
        ax1.set_title("Chromatogram of " + str(name), fontsize=25)
        plt.scatter(x=0, y=-20, color="white")

        # MW above graph columns=["ml", "UV/Vis", "MW"]
        V0_max = df_mAU["ml_mAU"].where(df_mAU["ml_mAU"] < float(V0)).max()
        df = df.where(df["ml"] > V0_max).dropna()
        i = 0
        while i <= len(df)-1:

            plt.text(df.iloc[i, 0], df.iloc[i, 1], str(df.iloc[i, 2]) + " kDa", fontsize=15)
            i = i +1


        # if Conductivity column was present and wanted
        if "mS/cm" in list(df_2.columns):
            l2 = ax2.scatter(data=df_2, x="Volume", y="Conductivity", color="black", label="Conductivity")
            ax2.set_ylabel("Conductivity [mS/cm]", fontsize=15)
            labels = [l1, l2]
            labs = [l.get_label() for l in labels]
            plt.legend(labels, labs, loc=0)
            AlignPlot.align_yaxis(ax1, 0, ax2, 0)

        # if Fractions column was present and wanted
        if "Fractions" in list(df_3.columns):
            plt.text(0.0, -20.0, "Fractions:", fontsize=15)
            p = 0
            while p <= (len(df_3) - 1):
                plt.text(float(df_3.iloc[p, 0]), -20.0, df_3.iloc[p, 1])
                p = p + 1

        plt.savefig(str(path) + str(name) + "_hplc.png", dpi=400, bbox_inches="tight")




#Terminal input (3 commands)
#data = sys.argv[1:]
#path= data[[0]]
#name = pd.read_fwf(data[[1]])
#plot_name = data[[2]]


# for testing on my windows surface only
path = "C:\\Users\\Feiler Werner\\Desktop\\Skerra_data\\HPLC\\"
name_excel = "29112022 WF MBP LepR2D PDI"
name = "MBP LepR2D PDI"

config_file = "HPLC.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

# HPLC configuration
type_column = config["HPLC_config"]["type"]
conductivity = config["HPLC_config"]["conductivity"]
V0 = float(config["HPLC_config"]["V0"])
Vtotal = float(config["HPLC_config"]["Vtotal"])
buffer = config["HPLC_config"]["buffer"]
graph_color = config["HPLC_config"]["graph_color"]


# SEC standard to calculate the molecular weight
config_file = "SEC_standard.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

a = float(config["regression_parameters"]["a"])
b = float(config["regression_parameters"]["b"])


array_df = HPLC.sec_norm(path = path, name_excel = name_excel)
df_mAU = array_df[0]
df_peaks = HPLC.peak_picker(df_mAU)
df_MW = HPLC.calculate_MW(a, b, V0, V_total = Vtotal, V_elu_df = df_peaks, df=df_mAU)
HPLC.hplc_plot(array_df, df = df_MW, name = name, path = path, color = graph_color)

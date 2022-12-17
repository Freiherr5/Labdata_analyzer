import pandas as pd
import AlignPlot
import matplotlib.pyplot as plt
from configparser import ConfigParser
import math
import sys
from scipy import signal


class HPLC:

    def __init__(self, path, name_file, name, df, a, b, V0, V_total, V_elu_df, array, array_df, color, file_type):
        self.color = color
        self.file_type = file_type    # defines the file type that needs to be extracted
        self.name = name      # name of the plot + Heading
        self.array = array    # array with local/global maxima
        self.array_df = array_df
        self.path = path
        self.name_file = name_file
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
            UV_Vis_signal = float(df.iloc[int(V_elu_df.values[i]), 1]) + float(df.iloc[int(V_elu_df.values[0]), 1])*0.10
            array_ml_MW.append([ml_i, UV_Vis_signal, MW_i])
            i = i + 1

        df_ml_MW = pd.DataFrame(array_ml_MW, columns=["ml", "UV/Vis", "MW"])
        return df_ml_MW


    def sec_norm(path, name_file, file_type):
        # clean dataframe for plotting
        if file_type == "xls":
            df_all = pd.read_excel(str(path) + str(name_file) + "." + str(file_type), header = 2)
        if file_type == "txt":
            df_all = pd.read_excel(str(path) + str(name_file) + "." + str(file_type), header = 1)
        array_columns = list(df_all.columns)    #creates array with all column names, search for "mAU" and optional "mS/cm", "(Injections)" = Fractions

        #find positions of the columns of interest and get both columns: volume [ml] (on the left side of the column of interest)

        array_of_interest = []

        # dataframe part that is always present:
        ml = array_columns[0]
        mAU = array_columns[1]
        df_mAU = df_all[[ml, mAU]].copy()
        array_of_interest.append(df_mAU.rename(columns={ml : "ml_mAU", mAU : "mAU"}))

        if "%" in array_columns:
            index_mS = array_columns.index("%")
            ml = array_columns[index_mS-1]
            mS = array_columns[index_mS]
            df_mS = df_all[[ml, mS]].copy()
            array_of_interest.append(df_mS.rename(columns={ml : "ml_%", mS : "% of elution-buffer"}))

        if "(Fractions)" in array_columns:
            index_In = array_columns.index("(Fractions)")
            ml = array_columns[index_In - 1]
            In = array_columns[index_In]
            df_In = df_all[[ml, In]].copy().dropna()
            array_of_interest.append(df_In.rename(columns={ml: "ml_In", In: "Fractions"}))

        if "Fractions" in array_columns:
            index_In = array_columns.index("Fractions")
            ml = array_columns[index_In - 1]
            In = array_columns[index_In]
            df_In = df_all[[ml, In]].copy().dropna()
            array_of_interest.append(df_In.rename(columns={ml: "ml_In", In: "Fractions"}))

        return array_of_interest


    def hplc_plot(array_df, df, name, path, color):

        # unpack DataFrames from the array and give them a
        df_mAU = array_df[0]
        df_2 = ["-"]
        df_3 = ["-"]

        if len(array_df) == 2:
            df_2 = array_df[1]

        if len(array_df) == 3:
            df_3 = array_df[2]

        if list(df_2.columns)[1] == "Fractions":
            df_3 = df_2

        # generates the plot
        plt.figure(figsize=(25, 10))
        ax1 = plt.subplot(1, 1, 1)

        # if Conductivity column was present and wanted
        if "%" in list(df_2.columns):
            ax2 = ax1.twinx()

        l1 = ax1.scatter(data=df_mAU, x="ml_mAU", y="mAU", color=str(color), label="UV/Vis signal")

        ax1.set_ylabel("UV/Vis signal [mAU]", fontsize=15)
        ax1.set_xlabel("Volume [ml]", fontsize=15)
        ax1.set_title("Chromatogram of " + str(name), fontsize=25)
        plt.scatter(x=0, y=-20, color="white")

        if conductivity.lower() != "yes":
            # MW above graph columns=["ml", "UV/Vis", "MW"]
            V0_max = df_mAU["ml_mAU"].where(df_mAU["ml_mAU"] < float(V0)).max()
            df = df.where(df["ml"] > V0_max).dropna()
            i = 0
            while i <= len(df)-1:
                plt.text(df.iloc[i, 0], df.iloc[i, 1] + (df_mAU["mAU"].max()*0.01), str(df.iloc[i, 2]) + " kDa", fontsize=10, va="bottom")
                i = i +1


        # if Conductivity column was present and wanted
        if "%" in list(df_2.columns):
            l2 = ax2.scatter(data=df_2, x="ml_%", y="% of elution-buffer", color="black", label="% elution-buffer")
            ax2.set_ylabel("Percent of elution-buffer", fontsize=15)
            labels = [l1, l2]
            labs = [l.get_label() for l in labels]
            plt.legend(labels, labs, loc=0)
            AlignPlot.align_yaxis(ax1, 0, ax2, 0)

        # if Fractions column was present and wanted
        if "Fractions" in list(df_3.columns):
            plt.text(0.0, -20.0, "Fractions:", fontsize=15)
            p = 0
            while p <= (len(df_3) - 1):
                plt.text(float(df_3.iloc[p, 0]), -20.0, df_3.iloc[p, 1], fontsize=15, ha="center")
                p = p + 1

        # descriptive elements of the plot: column, buffer, V0 location
        config_file = "HPLC.ini"
        config = ConfigParser()
        config.read(config_file)
        config.sections()

        if conductivity.lower() != "yes":               # V0 indication for SEC
            V0_x = float(config["HPLC_config"]["V0"])
            V0_y = df.iloc[0, 1]
            x1, y1 = [V0_x, V0_x], [0, V0_y]
            plt.plot(x1, y1, "--", color = "black")
            ax1.text(V0_x, V0_y * (-0.05), "V0 = " + str(V0) + " ml", ha="right")


        type = config["HPLC_config"]["type"]
        buffer = config["HPLC_config"]["buffer"]
        y_max = df_mAU["mAU"].max()
        x_max = df_mAU["ml_mAU"].max()
        ax1.text(x_max, y_max, "Column: " + type, fontsize=10, ha="right")
        ax1.text(x_max, y_max - (y_max * 0.03), "Buffer:" + config[buffer]["run_b"], fontsize=10, ha="right")

        plt.savefig(str(path) + str(name) + "_hplc.png", dpi=400, bbox_inches="tight")




#Terminal input (3 commands)
#data = sys.argv[1:]
#path= data[[0]]
#name_excel = pd.read_fwf(data[[1]])
#name = data[[2]]


# for testing on my windows surface only
path = "C:\\Users\\Feiler Werner\\Desktop\\Skerra_data\\HPLC\\"
name_file = "29112022 WF MBP LepR2D PDI"
file_type = "xls"
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

array_df = HPLC.sec_norm(path = path, name_file = name_file, file_type = file_type)

if conductivity.lower() != "yes":
    df_mAU = array_df[0]
    df_peaks = HPLC.peak_picker(df_mAU)
    df_MW = HPLC.calculate_MW(a, b, V0, V_total = Vtotal, V_elu_df = df_peaks, df=df_mAU)
else:
    df_MW = "none for conductivity"
HPLC.hplc_plot(array_df, df = df_MW, name = name, path = path, color = graph_color)

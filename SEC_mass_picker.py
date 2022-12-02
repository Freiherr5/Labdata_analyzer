import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser
import math

def standard_weight_SEC(path, file_name, V0, V_total, color, heading, buffer, type):
    df_mass_standard = pd.read_csv(path + file_name + ".txt")

    # addition of new parameters to the dataframe; base form (name, abbreviation, MW, ml)

    i = 0
    array = []
    while i <= len(df_mass_standard)-1:
        # calculate Kav = (Vsample_elution - V0) / (V_total - V0)
        Kav = (float(df_mass_standard.iloc[i, 3]) - float(V0)) / (float(V_total) -float(V0))
        # calculate the logarithmic weight (kDa)
        logMW = math.log10(df_mass_standard.iloc[i, 2])
        array.append([Kav, logMW])
        i = i+1

    df_array = pd.DataFrame(array, columns=["Kav", "logMW"])
    df_mass_standard = df_mass_standard.join(df_array)
    #new df_mass_standard --> name, abbreviation, MW, ml, Kav, logMW


    plt.figure(figsize=(10, 10))
    ax = plt.subplot(1, 1, 1)
    ax.scatter(data=df_mass_standard, x = "logMW", y = "Kav", color = color)
    y_max = float(df_mass_standard["Kav"].max())
    x_max = float(df_mass_standard["logMW"].max()) * 1.10

    ax.text(x_max, y_max, "Index", fontsize = 10, fontweight = "semibold", ha= "left")
    ax.set_title(heading, fontsize=25)
    ax.set_ylabel("$K_{av}$", fontsize=15)
    ax.set_xlabel("Molecular Weight [Da]", fontsize=15)

    y = df_mass_standard["Kav"].to_numpy()
    x = df_mass_standard["logMW"].to_numpy()
    m, b = np.polyfit(x, y, 1)
    regression_formula = str(round(m, 3)) + " * x + " + str(round(b,3))
    plt.plot(x, m*x+b, "--", color = color)
    plt.text(float(df_mass_standard["logMW"].max()), float(df_mass_standard["Kav"].max()), "Regression: " + str(regression_formula), ha= "right")
    plt.xticks([1.0, 2.0, 3.0], ["10,000 Da", "100,000 Da", "1,000,000 Da"])

    i = 0
    while i <= len(df_mass_standard)-1:
        # text above each datapoint
        ax.text(df_mass_standard.iloc[i, 5], df_mass_standard.iloc[i, 4]+df_mass_standard.iloc[0, 4]*0.01, df_mass_standard.iloc[i, 1], fontsize = 10, ha="center")
        # add legend on the top right to show context
        ax.text(x_max, y_max - (y_max*((1.5+i)/50)), df_mass_standard.iloc[i, 1] + " = " + df_mass_standard.iloc[i, 0] + " (" + str(df_mass_standard.iloc[i, 2]) + " kDa )", fontsize = 10, ha = "left")
        i = i+1
    ax.text(x_max, y_max - (y_max * ((1.5 + i+3) / 50)), "Column: " + type, fontsize=10, ha="left")
    ax.text(x_max, y_max - (y_max * ((1.5 + i+4) / 50)), "Buffer:" + config[buffer]["run_b"], fontsize=10, ha="left")
    plt.savefig(str(path) + str(file_name) + ".png", dpi=400, bbox_inches="tight")


path = "C:\\Users\\Feiler Werner\\Desktop\\Skerra_data\\SEC\\"
file_name = "SEC standards"
heading = "SEC standard proteins"



config_file = "HPLC.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

V0 = config["HPLC_config"]["V0"]
V_total = config["HPLC_config"]["Vtotal"]
type = config["HPLC_config"]["type"]
buffer = config["HPLC_config"]["buffer"]
color = config["HPLC_config"]["graph_color"]

standard_weight_SEC(path = path, file_name = file_name, heading = heading, color = color, V0 = V0, V_total = V_total, buffer = buffer, type = type)
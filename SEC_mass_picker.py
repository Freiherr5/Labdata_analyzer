import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser

def standard_weight_SEC(path, file_name):
    df_mass_standard = pd.read_fwf(path + file_name + ".txt", sep= ",")

    # addition of new parameters to the dataframe


    # calculate Kav = (Vsample_elution - V0) / (Vtotal - V0)

    # calculate the logarithmic weight (kDa)



    plt.figure(figsize=(10, 10))
    ax = plt.subplot(1, 1, 1)
    ax.scatter(data=df_mass_standard)






config_file = "HPLC.ini"
config = ConfigParser()
config.read(config_file)
config.sections()

V0 = config["HPLC_config"]["V0"]
V_total = config["HPLC_config"]["Vtotal"]
type = config["HPLC_config"]["type"]
buffer = config["HPLC_config"]["buffer"]
color = config["HPLC_config"]["graph_color"]
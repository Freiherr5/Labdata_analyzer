import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance
from configparser import ConfigParser
from scipy import signal


config_file = "GelAnalyzer.ini"
config = ConfigParser()
config.read(config_file)
config.sections()
gel_slots = config["gel_slots"]["gel_slots"]


#get the gel slice with only the marker
def get_marker_position(gel_slots, x_shift_marker, marker, set_file_name, set_path_folder):

    im = Image.open(str(set_path_folder) + str(set_file_name) + ".jpg")

    width, height = im.size

    width_marker = int(width) / int(gel_slots)

    # create an array with the gel slice (left side) of the maker, determine the concentration of the signal (peak) and set it as point for the window

    im_grey_pre = im.convert("L")
    # for bright agarose gels the picture needs to be inverted
    array_grey_pre = np.array(im_grey_pre)
    sum_grey_1D_x_axis = pd.DataFrame(array_grey_pre).sum(axis=0).to_numpy() # column wise adding of values, creates series of sums, then array
    peaks_x = pd.DataFrame(signal.find_peaks(sum_grey_1D_x_axis, prominence=5000)).transpose()[0]
    midpoint_marker = peaks_x[0]

    range_marker = width_marker * 0.13

    # cropping parameters for gel slice
    left = midpoint_marker - range_marker
    upper = 0
    right = midpoint_marker + range_marker
    lower = height

    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(5)

    im1 = im.crop((left, upper, right, lower))
    im_grey = im1.convert("L")

    im_grey.show()

    array_grey = np.array(im_grey)
    sum_grey_1D_y_axis = pd.DataFrame(array_grey).sum(axis=1).to_numpy()  # row wise adding of values, creates series of sums, then array (marker slice)
    peaks_y = pd.DataFrame(signal.find_peaks(sum_grey_1D_y_axis, prominence=350)).transpose()[0]
    peaks_y_df = pd.DataFrame(peaks_y).where(peaks_y > height*0.1).dropna().reset_index(drop=True)
    #join the names of the molecular weights
    k = 0
    array_MW = []
    while k <= len(peaks_y_df)-1:
        inter_MW = config[str(marker)]["band"+str(k+1)]
        array_MW.append(inter_MW)
        k = k+1
    df_MW = pd.DataFrame(array_MW, columns= ["MW"])
    peaks_name = pd.concat([peaks_y_df, df_MW], axis=1)

    return peaks_name # pos 0 = position, pos 1 = molecular weight names


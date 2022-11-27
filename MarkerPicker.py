import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageEnhance
from configparser import ConfigParser


config_file = "GelAnalyzer.ini"
config = ConfigParser()
config.read(config_file)
config.sections()
gel_slots = config["gel_slots"]["gel_slots"]



#get the gel slice with only the marker
def get_marker_postion(gel_slots, x_shift_marker, marker, set_file_name, set_path_folder):

    im = Image.open(str(set_path_folder) + str(set_file_name) + ".jpg")

    width, height = im.size

    width_marker = int(width) / int(gel_slots)
    midpoint_marker = width_marker/2 + x_shift_marker            #shifting the window along the x axis to only focus on the marker
    range_marker = width_marker * 0.1

    #cropping parameters for gel slice
    left = midpoint_marker - range_marker
    upper = 0
    right = midpoint_marker + range_marker
    lower = height

    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.2)

    im1 = im.crop((left, upper, right, lower))
    im_grey = im1.convert("1")


    im_grey.show()


    array_grey = np.array(im_grey)
    sum_grey_1D = pd.DataFrame(array_grey).sum(axis=1)
    #print(sum_grey_1D.min())    #11
    #print(sum_grey_1D.max())    #38

    # separate array in chunks
    array_chunk = []
    factor = 5
    i = 1
    while (i)*factor <= height-factor:
        one_chunk = sum_grey_1D[i*factor:(i*factor+factor)].mean()
        array_chunk.append([i*factor+factor, one_chunk])
        i=i+1

    chunk_df = pd.DataFrame(array_chunk, columns=["pos_bottom", "chunks"])

    cut_off = sum_grey_1D.max() * 0.70

    df_bigger_cutoff = chunk_df[chunk_df["chunks"] > cut_off]

    # get the low cutoff rows of each band (look for continious index count and take the lowest entry as position point of the band in the gel)
    where_marker_array = []
    i = 0
    k = 1
    while i <= len(df_bigger_cutoff)-2:

        if df_bigger_cutoff.iloc[i, 0] + 5 != df_bigger_cutoff.iloc[i+1, 0]:
            where_marker_array.append([config[marker]["band" + str(k)], df_bigger_cutoff.iloc[i, 0]])
            k = k+1
        i = i+1

    df_marker_postion = pd.DataFrame(where_marker_array)
    return df_marker_postion

#compare original and post processing of the marker

#fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(3,8), sharex= True, sharey=True)
#ax1.imshow(im1)
#ax1.set_title("original")
#ax1.axis("off")
#ax2.imshow(im_grey)
#ax2.set_title("grey scale")
#ax2.axis("off")
#plt.savefig(str(set_path_folder) + "correction.png", dpi=400, bbox_inches="tight")


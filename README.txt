General structure of the data analyser:

The file contains 7 scripts:

BacGrowth.py       --> plots growth of the bacteria

HPLC.py            --> High performance liquid chromatography Data (UV/Vis and conductivity + fractions (optional) to running volume
                       Based on SEC_mass_picker.py it can automatically determine the molecular weight of proteins (SEC only)
AlignPlot.py       --> Coordinates mAU (UV/Vis) signal and mS/cm (conductivity) of the HPLC plot (dual y-axis)
(library)

SEC_mass_picker.py --> Chromatography column of the HPLC system need standardized values to determine the molecular weight of proteins
                       (only for size exclusion chromatography (SEC)):
                       calculates based on the elution-volume for all standards a linear regression (log10)

GelAnalyzer.py     --> Script that annotates gels based on a configuration file. Furthermore, the protein molecular weight marker is
+ MarkerPicker.py      automatically annotated using a value evaluation process of a small slice of the marker region (marker is always
                       positioned on the left hand side of the gel(MarkerPicker.py)).
                       The configuration file allows for a quick modulation of the parameters if needed.


StandardConfig.py  --> Allows for a variety of functions:
                       - can detect path of the folder its script is located in
                       - can create a folder with a specific directory
                       - can extract .txt file names within a target folder for automated processing
(library; currently not used)

Configfiles (.ini) are implemented to configurate base parameters


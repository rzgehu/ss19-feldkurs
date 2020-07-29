"""Nicolas Gampierakis 2019
Converts IAO files into a readable format for raster manipulation.
"""

import pandas as pd
import numpy as np
import re

# Read in raster files
path_file = "./data/mid/mid_raster_y2d.txt"

output = open("./data/output.txt","w")
input = open(path_file)

for line in input:
    output.write(re.sub(r'\n ', r'\n', line))
    output.write(re.sub(r'  ', r'\t', line))

input.close()
output.close()
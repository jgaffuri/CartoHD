import math
from math import ceil, hypot, floor
import subprocess
import numpy as np
import rasterio
import geopandas as gpd
from scipy.ndimage import binary_dilation, gaussian_filter, binary_erosion
import json
import os



def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout: print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)


file = "/home/juju/workspace/CartoHD/tmp/lu/output/45000_95000/dsm_vegetation.tif"



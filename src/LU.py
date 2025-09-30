from cartoHD import run_command, cartoHDprocess
import os
import geopandas as gpd
import os
import shutil
import requests
import zipfile
from urllib.parse import urlparse


'''
https://data.public.lu/fr/datasets/lidar-2024-releve-3d-du-territoire-luxembourgeois/#/resources

[1] - Autre
[2] - Sol
[3] - Végétation basse (< 2,5 m)
[4] - Végétation moyenne (2,5 m - 5 m)
[5] - Végétation haute (> 5 m)
[6] - Bâtiments
[7] - Bruit et artefacts
[9] - Eau
[13] - Ponts, Passerelles, Viaducs
[15] - Lignes à haute tension

'''

ta = "/home/juju/geodata/lidar/lu/lidar2024-ta.gpkg"
df = gpd.read_file(ta)
df = dict(zip(df['Fichier'], df['DownloadLink']))
#83500_82500 : https://data.public.lu/fr/datasets/r/a1b312e3-ed02-4a27-bb73-5276417d8a7a


#tmp/lu/input/84000_79500.laz


tmp = "/home/juju/workspace/CartoHD/tmp/lu/"
input = tmp+"input/"

# set tile bounds
#xmin xmax ymin ymax
xmin = 83000; ymin = 79500; size = 1500

# check files are there
for x in range(xmin, xmin+size, 500):
    for y in range(ymin, ymin+size, 500):
        code = str(x)+"_"+str(y)
        file = input + code + ".laz"
        print(code)
        if os.path.exists(file): continue
        print("do not exist!")
        downl_url = df[code]
        print(downl_url)

exit()


# output folder
output_folder = tmp + "output/" + str(xmin) + "_" + str(ymin) + "/"
os.makedirs(output_folder, exist_ok=True)

# Process PDAL tile
if not os.path.exists(output_folder + "dsm.tif"):
    print("Processing PDAL tile", xmin, ymin)
    bounds = "(["+str(xmin)+", "+str(xmin+size)+"],["+str(ymin)+", "+str(ymin+size)+"])"
    cartoHDprocess(tmp + "input/*.laz", output_folder, bounds = bounds, case="LU")

# copy project
if not os.path.exists(output_folder + "project_LU_bulk.qgz"):
    run_command(["cp", "src/project_LU_bulk.qgz", output_folder])

from cartoHD import run_command, cartoHDprocess
import os
import geopandas as gpd


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


ID tuile : Lidar2024_C024_R016
Tuile : C024/R016
Nom du fichier : lidar2024_c024_r016.zip
https://data.public.lu/fr/datasets/r/fc346700-41c9-477c-b08d-c82d08799726
Coordonnée X gauche-bas : 83000
Coordonnée Y gauche-bas : 79000


https://download.data.public.lu/resources/bd-l-lidar2024-releve-3d-du-territoire-luxembourgeois/20241129-132527/lidar2024-c001-r030.zip



"/home/juju/geodata/lidar/lu/lidar2024-ta.gpkg"

define extent on LU
decompose into tiles

for each tile:
    check if necessary data exists in "/tmp/lu/input/"
    download necessary data
    launch cartohd process
    make tile tiff in /tmp/lu/tiff/

    draw BDTOPO elements
    make enriched tiff in /tmp/lu/tiff/

do web tiling of all tiffs

'''

ta = "/home/juju/geodata/lidar/lu/lidar2024-ta.gpkg"
df = gpd.read_file(ta)
df = dict(zip(df['Fichier'], df['DownloadLink']))
print(df)
exit()


'''
Fichier
Dossier
DownloadLink
83500_82500
Lidar2024_C024_R018
https://data.public.lu/fr/datasets/r/a1b312e3-ed02-4a27-bb73-5276417d8a7a
'''



tmp = "/home/juju/workspace/CartoHD/tmp/lu/"

# set tile bounds
#xmin xmax ymin ymax
xmin = 83000; ymin = 79000; size = 1500

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

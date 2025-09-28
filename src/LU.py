from cartoHD import run_command, cartoHDprocess
import os


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



tmp = "/home/juju/workspace/CartoHD/tmp/lu/"

input_lidar_data = tmp + "input/"
os.makedirs(input_lidar_data, exist_ok=True)

#xmin xmax ymin ymax
xmin = 83000
ymin = 79000
size = 1500
bounds = "([83000, 84500],[79000, 80500])"
output_folder = tmp + "tiff/" + str(xmin) + "_" + str(ymin) + "/"
os.makedirs(output_folder, exist_ok=True)

# launch process
cartoHDprocess(input_lidar_data, output_folder, bounds = bounds, case="LU")


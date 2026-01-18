from cartoHD import run_command, cartoHDprocess
import os


#TODO
#processing.run("terrain_shading:Shadow depth", {'INPUT':'/tmp/processing_RHeEYq/7b63e916c7dc48d1aeb658a89ca78558/OUTPUT.tif','DIRECTION':315,'ANGLE':10,'SMOOTH':True,'OUTPUT':'TEMPORARY_OUTPUT'})
'''

1 Non classé
2 Sol
3 Végétation basse (0-50 cm)
4 Végétation moyenne (50 cm-1,50 m)
5 Végétation haute (+1,50 m)
6 Bâtiment
9 Eau
17 Tablier de pont

64 Sursol pérenne
66 Points virtuels
67 Divers - bâtis

'''


idf = "/home/juju/geodata/lidar/"
for f in ["niederanven"]:
    print(f)

    print("download")
    os.makedirs(idf+f+"/", exist_ok=True)
    #if f != "carcassonne":
    #run_command(["wget", "-i", idf+f+".txt", "-nc", "-P", idf+f+"/"])

    input_lidar_data = idf+f+"/*.laz"
    output_folder = "/home/juju/lidar_mapping/"+f+"/"
    #xmin xmax ymin ymax
    bounds = None #"([699000, 703000],[636000, 639000])"

    cartoHDprocess(input_lidar_data, output_folder, bounds = bounds, case="FR")

    print("copy QGIS project file")
    run_command(["cp", "src/project_LU.qgz", output_folder])

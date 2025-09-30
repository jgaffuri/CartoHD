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

def download_unzip_and_cleanup(zip_url, local_folder):
    """
    Downloads a ZIP file from a URL, unzips it, moves the contents to the parent folder,
    and deletes the ZIP file and the empty unzipped folder.

    Args:
        zip_url (str): URL of the ZIP file to download.
        local_folder (str): Local folder path where the ZIP will be downloaded and unzipped.
    """
    # Create the local folder if it doesn't exist
    os.makedirs(local_folder, exist_ok=True)

    # Extract the filename from the URL
    parsed_url = urlparse(zip_url)
    zip_filename = os.path.basename(parsed_url.path)
    zip_path = os.path.join(local_folder, zip_filename)

    # Download the ZIP file
    print(f"Downloading {zip_filename}...")
    response = requests.get(zip_url, stream=True)
    response.raise_for_status()
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Unzip the file
    print(f"Unzipping {zip_filename}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(local_folder)

    # Delete the ZIP file
    os.remove(zip_path)
    print(f"Deleted {zip_filename}.")

    # The unzipped folder is the first (and only) folder in the local_folder
    # (assuming the ZIP contains a single folder)
    unzipped_folder = None
    for item in os.listdir(local_folder):
        item_path = os.path.join(local_folder, item)
        if os.path.isdir(item_path):
            unzipped_folder = item_path
            break

    if unzipped_folder:
        # Move all files from the unzipped folder to the parent folder
        for file in os.listdir(unzipped_folder):
            src = os.path.join(unzipped_folder, file)
            dst = os.path.join(local_folder, file)
            shutil.move(src, dst)
        print(f"Moved files from {os.path.basename(unzipped_folder)} to {local_folder}.")

        # Delete the now-empty unzipped folder
        os.rmdir(unzipped_folder)
        print(f"Deleted empty folder {os.path.basename(unzipped_folder)}.")
    else:
        print("No unzipped folder found.")



ta = "/home/juju/geodata/lidar/lu/lidar2024-ta.gpkg"
df = gpd.read_file(ta)
df = dict(zip(df['Fichier'], df['DownloadLink']))
#83500_82500 : https://data.public.lu/fr/datasets/r/a1b312e3-ed02-4a27-bb73-5276417d8a7a


#tmp/lu/input/84000_79500.laz


tmp = "/home/juju/workspace/CartoHD/tmp/lu/"
input = tmp+"input/"

# set tile bounds
#xmin xmax ymin ymax
xmin = 85000; ymin = 79000; size = 500

# check files are there
for x in range(xmin, xmin+size, 500):
    for y in range(ymin, ymin+size, 500):
        code = str(x)+"_"+str(y)
        if os.path.exists(input + code + ".laz"): continue
        downl_url = df[code]
        if downl_url is None: continue
        download_unzip_and_cleanup(zip_url = downl_url, local_folder=input)


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

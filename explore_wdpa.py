import geopandas as gpd
import os

folder_0 = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\New folder\DIGITAL_TWIN_ISLANDS\02_data_raw\WDPA_extracted_0"

shp_files = [f for f in os.listdir(folder_0) if f.endswith('.shp')]
print(shp_files)
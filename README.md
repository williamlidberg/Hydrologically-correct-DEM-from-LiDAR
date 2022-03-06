# Hydrologically-correct-DEM-from-LiDAR
How to make a hydrollogically compatible DEM ffrom a national LiDAR scan
The raw LiDAR data was downloaded from the Swedish mapping, cadastral and land registration authority (Lantmäteriet): https://www.lantmateriet.se/en/maps-and-geographic-information/geodataprodukter/produktlista/laserdata-nedladdning-skog/

Whitebox tools uses data from nearby tiles but in order for this to work all tiles need to be stored in the same directory. The raw data is stored in  multiple subdirectories as .laz files. Use the script pool_laz_files.py to copy all tiles in the same directory. 

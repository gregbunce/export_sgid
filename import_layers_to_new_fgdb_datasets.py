import arcpy
import os
from datetime import datetime

'''
use python 2.7 (or update table paths to pro)

Overview:
This script was written as a one-off by Greg Bunce on 09/18/2019. It imports the requested feature classes (or tables) that currently reside in the 
SGID Internal enterprise database and loads them into a staging fgdb. Eventually, these are the layers that will be imported into the new sgid enterprise database.

Notes on running this script:
1. This code expects that you have already created a destination file geodatabase.
2. You will need to provide a list of Owner.FeatureClass in a text file that is formatted like this (use script in this repo to create this list)
    BOUNDARIES.Utah
    CADASTRE.LandOwnership
    ECONOMY.EnterpriseZones
3. Remember to set the following variables below to match your machine's configuration: 
    'destination_fgdb'
    'source_file'
'''

#: set these variables:
destination_fgdb = "C:\\temp\\SGID_backup_20220411.gdb"
source_layer_txt_file = open("L:\\agrc\users\\gbunce\share\\scripts_code\\export_sgid\\sgid_fc_list.txt", "r")
now = datetime.now().strftime('%Y%m%d_%H%M')
log_file = open("C:\\Temp\\sgid_migration_import_log_" + now + ".txt", 'w')
log_file.writelines("This report was generated on " + str(datetime.now()) + "\n")
log_file.writelines("The output here is from the import_layers_to_new_datasets.py script that was used during the 2019 SGID10 Migration process.\n\n")
log_file.writelines("The following tables/featureclasses were NOT imported into the file geodatabase because they already existed in there:" + "\n")

#: create a list from input file of feature classes with owner
source_list = []
source_list = source_layer_txt_file.readlines()

for tables in source_list:
    #: split on dot to get feature dataset and feature class
    owner_name = tables.split(".")[0].strip()
    print(owner_name)
    table_name = tables.split(".")[1].strip()
    print(table_name)
    table_full_path = "Database Connections\internal@SGID@internal.agrc.utah.gov.sde/SGID." + owner_name + "." + table_name

    #: create a feature dataset (if it doesn't already exist) for each owner type
    if not arcpy.Exists(os.path.join(destination_fgdb, owner_name)):
        #: if the feature dataset does not exist then create it
        print("creating feature dataset for " + owner_name + " as it does not yet exist in the db.")
        arcpy.CreateFeatureDataset_management(out_dataset_path=destination_fgdb, out_name=owner_name, spatial_reference="PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")

    #: import the tables in the text file list.
    desc = arcpy.Describe(table_full_path)

    #: check if listed table is standalone table:
    if desc.dataType == 'Table':
        # continue #: use this option if you don't want to import non-feature classes (aka: tables).
        #: check if table exists before importing it.
        if not arcpy.Exists(os.path.join(destination_fgdb, owner_name + "_" + table_name)):
            print("importing table " + owner_name + "_" + table_name + " into the db...")
            arcpy.TableToTable_conversion(in_rows=table_full_path, out_path=destination_fgdb, out_name=owner_name + "_" + table_name)
        else:
            print("Did not import table " + tables + " becuase it already exists in the db.")
            log_file.write("   Table: " + tables + "\n")
    #: check if listed table is feature class.
    if desc.dataType == 'FeatureClass':
        #: check if feature class exists before importing it.
        if not arcpy.Exists(os.path.join(destination_fgdb, owner_name, table_name)):
            #: if the feature dataset does not exist then create it
            print("importing feature class " + tables + " into the db...")
            arcpy.FeatureClassToFeatureClass_conversion(in_features=table_full_path, out_path=os.path.join(destination_fgdb, owner_name), out_name=table_name)
        else:
            print("Did not import feature class " + tables + " becuase it already exists in the db.")
            log_file.write("   FeatureClass: " + tables + "\n")

log_file.close()
print("Done!")
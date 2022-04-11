import arcpy
import os

arcpy.env.workspace = "Database Connections/internal@SGID@internal.agrc.utah.gov.sde"

#: on local machine
#log_file = open("C:\\Users\\gbunce\\Documents\\projects\\export_sgid_to_fgdb\\sgid_fc_list.txt", 'w')
#: on network share
log_file = open("L:\\agrc\\users\\gbunce\\share\\scripts_code\\export_sgid\\sgid_fc_list.txt", 'w')

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        log_file.writelines(path + "\n")
        print path
log_file.close()

        
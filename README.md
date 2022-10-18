use python 2.7 (or update table paths to pro)

Overview:
This script was written as a one-off by Greg Bunce on 09/18/2019. It imports the requested feature classes (or tables) that currently reside in the Internal
SGID enterprise database and loads them into a staging esri fgdb. Eventually, these are the layers that will be imported into the new sgid enterprise database.

Notes on running this script:
1. This code expects that you have already created a destination file geodatabase.
2. You will need to provide a list of Owner.FeatureClass in the text file \\sgid_fc_list.txt. Use the \\print_sgid_fc_names.py script in the repo to create this list. Then use Notepad to remove ('replace') the unneeded info. In the end, the list should be formatted like this:
    BOUNDARIES.Utah
    CADASTRE.LandOwnership
    ECONOMY.EnterpriseZones
3. [optional: remove the ELEVATION Contour datasets from the list - these are huge datasets that don't change often.  also the high res streams?]
4. run \\import_layers_to_new_fgdb_datasets.py
5. then upload the file geodatabase backup to google drive here (agrc_public_share>long_terms_share>sgid>sgid_db_archives):
https://drive.google.com/drive/u/1/folders/1YJHcW9i2dOeNvrN56_87NRHG6RMcEu8-
...use 7-zip if file is larger than 4GB (https://www.7-zip.org/)

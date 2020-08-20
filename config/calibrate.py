'''
Override the default calibrate config parameters by putting them in here.
e.g.:
config.doAstrometry = False
'''
import os.path
ObsConfigDir = os.path.dirname(__file__)
config.doPhotoCal = False # Needs a cal_ref_cat
config.doAstrometry = False # Needs reference catalogue ingested
# Reference catalogs
#The following was copied from obs_subaru and manages conflicts between gen2 and gen3
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
    # This is the Gen2 configuration option.
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_vist2020"

# These are the Gen3 configuration options for reference catalog name.
config.connections.photoRefCat = "ps1_pv3_3pi_vist2020"
config.connections.astromRefCat = "ps1_pv3_3pi_vist2020"


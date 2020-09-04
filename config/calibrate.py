'''
Override the default calibrate config parameters. This is mainly concerned with setting 
the reference catalogue and colour terms for its use. Perhaps we can also tinker with 
values here to increase fraction of ccds that pass calibration.
'''
import os.path
ObsConfigDir = os.path.dirname(__file__)

#config.doPhotoCal = False #False # Needs a cal_ref_cat
#config.doAstrometry = False # Needs reference catalogue ingested
# Demand astrometry and photoCal succeed
#config.requireAstrometry = True
#config.requirePhotoCal = True

# Reference catalogs
#The following was copied from obs_subaru and manages conflicts between gen2 and gen3
ref_cat = "ps1_pv3_3pi_20170110_vista" #_vista
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
    # This is the Gen2 configuration option.
    refObjLoader.ref_dataset_name = ref_cat

# These are the Gen3 configuration options for reference catalog name.
config.connections.photoRefCat = ref_cat
config.connections.astromRefCat = ref_cat

# These colorterms are for HSC, included as an example
colorterms = config.photoCal.colorterms
from lsst.pipe.tasks.colorterms import ColortermDict, Colorterm
colorterms.data["ps1*"] = ColortermDict(data={
    'g': Colorterm(primary="g", secondary="r", 
    c0=0.00730066, c1=0.06508481, c2=-0.01510570),
    'r': Colorterm(primary="r", secondary="i", 
    c0=0.00279757, c1=0.02093734, c2=-0.01877566),
    'i': Colorterm(primary="i", secondary="z", 
    c0=0.00166891, c1=-0.13944659, c2=-0.03034094),
    #'z2': Colorterm(primary="z", secondary="y", 
    #c0=-0.00907517, c1=-0.28840221, c2=-0.00316369),
    #'y2': Colorterm(primary="y", secondary="z", 
    #c0=-0.00156858, c1=0.14747401, c2=0.02880125),
    'z': Colorterm(primary="z", secondary="y", 
    c0=-0.0, c1=-0.0, c2=-0.0),
    'y': Colorterm(primary="y", secondary="z", 
    c0=-0.0, c1=0.0, c2=0.0),
    'j': Colorterm(primary="j", secondary="y",   #PLACEHOLDER
    c0=-0.0, c1=0.0, c2=0.0),
    'h': Colorterm(primary="h", secondary="y",   #PLACEHOLDER
    c0=-0.0, c1=0.0, c2=0.0),
    'ks': Colorterm(primary="ks", secondary="y", #PLACEHOLDER
    c0=-0.0, c1=0.0, c2=0.0),
   
})
# For the HSC r2 and i2 filters, use the r and i values from the catalog
# for refObjLoader in (config.calibrate.astromRefObjLoader,
#                      config.calibrate.photoRefObjLoader,
#                      config.charImage.refObjLoader,
#                      ):
#     pass
#    refObjLoader.filterMap['r2'] = 'r'
#    refObjLoader.filterMap['i2'] = 'i'

for i in [
#        'base_GaussianFlux',
#        'base_SdssShape', #base_SdssShape is needed for PSF determination.
        #'base_ScaledApertureFlux',
#        'base_CircularApertureFlux',
        'base_Blendedness',
        #'base_LocalBackground',
        #'base_Jacobian',
        #'base_FPPosition',
        #'base_Variance',
        #'base_InputCount',
        #'base_SkyCoord',
]:
    config.measurement.plugins[i].doMeasure=False
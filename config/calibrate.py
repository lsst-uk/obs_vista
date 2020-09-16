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
ref_cat = "ps1_pv3_3pi_20170110_2mass" #_vista
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
    # This is the Gen2 configuration option.
    refObjLoader.ref_dataset_name = ref_cat

# These are the Gen3 configuration options for reference catalog name.
config.connections.photoRefCat = ref_cat
config.connections.astromRefCat = ref_cat
# These are gen2?:
config.photoCal.applyColorTerms=True
config.photoCal.photoCatName=ref_cat

# Taken from https://github.com/lsst/pipe_tasks/blob/master/python/lsst/pipe/tasks/colorterms.py:
# p' = primary + c0 + c1*(primary - secondary) + c2*(primary - secondary)**2
# VISTA-2MASS colour terms taken from https://arxiv.org/abs/1711.08805 eqn 5-9
# Z_V = J_2 + (0.86 ± 0.08) · (J − Ks)_2
# Y_V = J_2 + (0.46 ± 0.02) · (J − Ks)_2
# J_V = J_2 − (0.031 ± 0.006) · (J − Ks)_2
# H_V = H_2 + (0.015 ± 0.005) · (J − Ks)_2
# Ks_V = Ks_2 − (0.006 ± 0.007) · (J − Ks)_2

colorterms = config.photoCal.colorterms
from lsst.pipe.tasks.colorterms import ColortermDict, Colorterm
colorterms.data["ps1*"] = ColortermDict(data={
    #####HSC COLOUR TERMS FROM obs_subaru
    'HSC-G': Colorterm(primary="g", secondary="r", 
    c0=0.00730066, c1=0.06508481, c2=-0.01510570),
    'HSC-R': Colorterm(primary="r", secondary="i", 
    c0=0.00279757, c1=0.02093734, c2=-0.01877566),
    'HSC-I': Colorterm(primary="i", secondary="z", 
    c0=0.00166891, c1=-0.13944659, c2=-0.03034094),
    'HSC-Z': Colorterm(primary="z", secondary="y", 
    c0=-0.00907517, c1=-0.28840221, c2=-0.00316369),
    'HSC-Y': Colorterm(primary="y", secondary="z", 
    c0=-0.00156858, c1=0.14747401, c2=0.02880125),
    ####VISTA REF (NO COLOUR TERMS)
    #'z': Colorterm(primary="z", secondary="y", 
    #c0=-0.0, c1=-0.0, c2=-0.0),
    #'y': Colorterm(primary="y", secondary="z", 
    #c0=-0.0, c1=0.0, c2=0.0),
    #'j': Colorterm(primary="j", secondary="y",  
    #c0=-0.0, c1=0.0, c2=0.0),
    #'h': Colorterm(primary="h", secondary="y",   
    #c0=-0.0, c1=0.0, c2=0.0),
    #'ks': Colorterm(primary="ks", secondary="y", 
    #c0=-0.0, c1=0.0, c2=0.0),
    ####2MASS COLOUR TERMS - all from J, Ks - see above
    'VISTA-Z': Colorterm(primary="j", secondary="ks", 
    c0=0.0, c1=0.86, c2=-0.0),
    'VISTA-Y': Colorterm(primary="j", secondary="ks", 
    c0=0.0, c1=0.46, c2=0.0),
    'VISTA-J': Colorterm(primary="j", secondary="ks",   
    c0=0.0, c1=0.031, c2=0.0),
    'VISTA-H': Colorterm(primary="j", secondary="ks",   
    c0=0.0, c1=0.015, c2=0.0),
    'VISTA-Ks': Colorterm(primary="j", secondary="ks", 
    c0=0.0, c1=-0.006, c2=0.0),
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
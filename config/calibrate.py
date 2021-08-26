'''
Override the default calibrate config parameters. This is mainly concerned with setting 
the reference catalogue and colour terms for its use. Perhaps we can also tinker with 
values here to increase fraction of ccds that pass calibration.
'''
import os.path
ObsConfigDir = os.path.dirname(__file__)

# config.doPhotoCal = False #False # Needs a cal_ref_cat
# config.doAstrometry = False # Needs reference catalogue ingested
# Demand astrometry and photoCal succeed
#config.requireAstrometry = True
#config.requirePhotoCal = True

# Reference catalogs
# The following was copied from obs_subaru and manages conflicts between gen2 and gen3
ref_cat = "ps1_pv3_3pi_20170110_vista"  
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
    # This is the Gen2 configuration option.
    refObjLoader.ref_dataset_name = ref_cat

# These are the Gen3 configuration options for reference catalog name.
config.connections.photoRefCat = ref_cat
config.connections.astromRefCat = ref_cat

config.photoCal.applyColorTerms = True
config.photoCal.photoCatName = ref_cat
config.photoCal.match.matchRadius = 2.0
config.photoCal.match.sourceSelection.doFlags = False
# Apply unresolved limitation?
config.photoCal.match.sourceSelection.doUnresolved = False
# List of source flag fields that must NOT be set for a source to be used.
config.photoCal.match.sourceSelection.flags.bad = [
    # 'base_PixelFlags_flag_edge',
    # 'base_PixelFlags_flag_interpolated',
    # 'base_PixelFlags_flag_saturated',
]

config.doPhotoCal = True
config.doAstrometry = True

config.photoCal.colorterms.load(os.path.join(ObsConfigDir, 'colorterms.py'))


for i in [
        # 'base_GaussianFlux',
        # 'base_SdssShape', #base_SdssShape is needed for PSF determination.
        # 'base_ScaledApertureFlux',
        # 'base_CircularApertureFlux',
        'base_Blendedness',
        # 'base_LocalBackground',
        # 'base_Jacobian',
        # 'base_FPPosition',
        # 'base_Variance',
        # 'base_InputCount',
        # 'base_SkyCoord',
]:
    config.measurement.plugins[i].doMeasure = False


# Astrometry
# Raise an exception if astrometry fails? Ignored if doAstrometry false.
config.requireAstrometry = False  

# List of flags which cause a source to be rejected as bad
config.astrometry.sourceSelector['astrometry'].badFlags = [
    'base_PixelFlags_flag_edge',
    'base_PixelFlags_flag_interpolatedCenter',
    'base_PixelFlags_flag_saturatedCenter',
    'base_PixelFlags_flag_crCenter',
    'base_PixelFlags_flag_bad'
]

config.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['astrometry'].sourceFluxType = 'Ap'

# Minimum allowed signal-to-noise ratio for sources used for matching (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['astrometry'].minSnr = 0.0

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['matcher'].sourceFluxType = 'Ap'

# Minimum allowed signal-to-noise ratio for sources used for matching (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['matcher'].minSnr = 0.0

# Exclude objects that have saturated, interpolated, or edge pixels using PixelFlags. For matchOptimisticB set this to False to recover previous matcher selector behavior.
config.astrometry.sourceSelector['matcher'].excludePixelFlags = False

# specify the minimum psfFlux for good Psf Candidates
config.astrometry.sourceSelector['objectSize'].fluxMin = 1000.0

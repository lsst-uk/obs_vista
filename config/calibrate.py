'''
Override the default calibrate config parameters. This is mainly concerned with setting 
the reference catalogue and colour terms for its use. 
'''
import os.path
from lsst.meas.astrom import MatchOptimisticBConfig
from lsst.meas.astrom import MatchPessimisticBConfig
from lsst.meas.algorithms import ColorLimit

ObsConfigDir = os.path.dirname(__file__)

# Reference catalogs
# The following was copied from obs_subaru and manages conflicts between gen2 and gen3
ref_cat = "ps1_pv3_3pi_20170110_vista"  
# Use PS1/VISTA for both astrometry and photometry.
config.connections.astromRefCat = ref_cat
config.astromRefObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia.
config.astromRefObjLoader.anyFilterMapsToThis = None

config.connections.photoRefCat = ref_cat
config.photoRefObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))

# number of iterations of fitter (which fits X and Y separately, and so benefits from a few iterations
# See Slack: https://lsstc.slack.com/archives/C2B6X08LS/p1586468459084600
#config.astrometry.wcsFitter.order = 4

# maximum number of iterations of match sources and fit WCSignored if not fitting a WCS
config.astrometry.maxIter=5

# Better astrometry matching
config.astrometry.matcher.numBrightStars = 150

config.doPhotoCal = True
config.doAstrometry = True

# Raise an exception if astrometry fails? Ignored if doAstrometry false.
config.requireAstrometry = True
# Raise an exception if photoCal fails? Ignored if doPhotoCal false.
config.requirePhotoCal=True


#List of flags which cause a source to be rejected as bad
#config.astrometry.sourceSelector['science'].flags.bad=[]
#config.astrometry.sourceSelector['astrometry'].badFlags=[]
# config.astrometry.sourceSelector['astrometry'].badFlags = [
#     'base_PixelFlags_flag_edge',
#     'base_PixelFlags_flag_interpolatedCenter',
#     'base_PixelFlags_flag_saturatedCenter',
#     'base_PixelFlags_flag_crCenter',
#     'base_PixelFlags_flag_bad'
# ]

config.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))

# Always use this reference catalog filter, no matter whether or what filter name is supplied to the loader. Effectively a trivial filterMap: map all filter names to this filter. This can be set for purely-astrometric catalogs (e.g. Gaia DR2) where there is only one reasonable choice for every camera filter->refcat mapping, but not for refcats used for photometry, which need a filterMap and/or colorterms/transmission corrections.
#config.astromRefObjLoader.anyFilterMapsToThis='g'

#Select objects with value less than this
#config.astrometry.referenceSelector.unresolved.maximum=None

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['astrometry'].sourceFluxType = 'Ap'

# Minimum allowed signal-to-noise ratio for sources used for matching (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['astrometry'].minSnr = 5.0

# If True then load reference objects and match sources but do not fit a WCS; this simply controls whether 'run' calls 'solve' or 'loadAndMatch'
#config.astrometry.forceKnownWcs=False

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['matcher'].sourceFluxType = 'Ap'

# Number of sigma (measured from the distribution) in magnitude for a potential reference/source match to be rejected during iteration.
#config.astrometry.magnitudeOutlierRejectionNSigma=0.0

# Minimum allowed signal-to-noise ratio for sources used for matching (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['matcher'].minSnr = 5.0

# Exclude objects that have saturated, interpolated, or edge pixels using PixelFlags. For matchOptimisticB set this to False to recover previous matcher selector behavior.
config.astrometry.sourceSelector['matcher'].excludePixelFlags=False

# specify the minimum psfFlux for good Psf Candidates. Unit=instrument flux
config.astrometry.sourceSelector['objectSize'].fluxMin=1000.0

# Minimum number of matched pairs; see also minFracMatchedPairs.
#config.astrometry.matcher.minMatchedPairs=10

# the maximum match distance is set to  mean_match_distance + matchDistanceSigma*std_dev_match_distance; ignored if not fitting a WCS
#config.astrometry.matcher.numRefRequireConsensus=2000

# the maximum match distance is set to  mean_match_distance + matchDistanceSigma*std_dev_match_distance; ignored if not fitting a WCS
#config.astrometry.matchDistanceSigma=2.0

config.photoCal.colorterms.load(os.path.join(ObsConfigDir, 'colorterms.py'))


for i in [
        # 'base_GaussianFlux',
        # 'base_SdssShape', #base_SdssShape is needed for PSF determination.
        # 'base_ScaledApertureFlux',
        # 'base_CircularApertureFlux',
        #'base_Blendedness',
        # 'base_LocalBackground',
        # 'base_Jacobian',
        # 'base_FPPosition',
        # 'base_Variance',
        # 'base_InputCount',
        # 'base_SkyCoord',
]:
    config.measurement.plugins[i].doMeasure = False
    
#VISTA colours
#colors = config.photoCal.match.referenceSelection.colorLimits
#colors["j-ks"] = ColorLimit(primary="j_flux", secondary="ks_flux", maximum=1.0)

config.photoCal.applyColorTerms = True
config.photoCal.photoCatName = ref_cat
config.photoCal.match.matchRadius = 1.0
config.photoCal.match.sourceSelection.doFlags = False
# Apply unresolved limitation?
config.photoCal.match.sourceSelection.doUnresolved = False
# List of source flag fields that must NOT be set for a source to be used.
config.photoCal.match.sourceSelection.flags.bad = [
    # 'base_PixelFlags_flag_edge',
    # 'base_PixelFlags_flag_interpolated',
    # 'base_PixelFlags_flag_saturated',
]

# Prevent spurious detections in vignetting areas
# config.detection.thresholdType = 'stdev'
# config.detection.thresholdValue = 10.0  # default=5.

#From obs subaru following error
config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.168
"""
Override the default calibrate configuration parameters for VIRCAM.

This configuration sets the VISTA Monster reference catalogue and
VIRCAM-specific astrometric, photometric, and measurement overrides.
"""

import os


obsConfigDir = os.path.dirname(__file__)

# Reference catalogs
ref_cat = "the_monster_20250219_vista"

config.connections.astromRefCat = ref_cat
config.astromRefObjLoader.load(os.path.join(obsConfigDir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia.)
config.astromRefObjLoader.anyFilterMapsToThis = None

config.connections.photoRefCat = ref_cat
config.photoRefObjLoader.load(os.path.join(obsConfigDir, "filterMap.py"))


# Set to match defaults currently used in HSC production runs (e.g. S15B)
config.astrometry.wcsFitter.numRejIter = 3
config.astrometry.wcsFitter.order = 3
config.astrometry.matcher.maxRotationDeg = 1.145916

# maximum number of iterations of match sources and fit WCSignored if
# not fitting a WCS
config.astrometry.maxIter=5

# Better astrometry matching
# config.astrometry.matcher.numBrightStars = 150

config.doPhotoCal = True
config.doAstrometry = True

# Raise an exception if astrometry fails? Ignored if doAstrometry false.
config.requireAstrometry = True
# Raise an exception if photoCal fails? Ignored if doPhotoCal false.
config.requirePhotoCal=True



# Always use this reference catalog filter, no matter whether or what
# filter name is supplied to the loader. Effectively a trivial
# filterMap: map all filter names to this filter. This can be set for
# purely-astrometric catalogs (e.g. Gaia DR2) where there is only one
# reasonable choice for every camera filter->refcat mapping, but not
# for refcats used for photometry, which need a filterMap and/or
# colorterms/transmission corrections.
# config.astromRefObjLoader.anyFilterMapsToThis='g'

# Select objects with value less than this
# config.astrometry.referenceSelector.unresolved.maximum=None

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['astrometry'].sourceFluxType = 'Ap'

# Minimum allowed signal-to-noise ratio for sources used for matching
# (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['astrometry'].minSnr = 5.0

# If True then load reference objects and match sources but do not fit
# a WCS; this simply controls whether 'run' calls 'solve' or
# 'loadAndMatch'
# config.astrometry.forceKnownWcs=False

# Type of source flux; typically one of Ap or Psf
config.astrometry.sourceSelector['matcher'].sourceFluxType = 'Ap'

# Number of sigma (measured from the distribution) in magnitude for a
# potential reference/source match to be rejected during iteration.
# config.astrometry.magnitudeOutlierRejectionNSigma=0.0

# Minimum allowed signal-to-noise ratio for sources used for matching
# (in the flux specified by sourceFluxType); <= 0 for no limit
config.astrometry.sourceSelector['matcher'].minSnr = 5.0

# Exclude objects that have saturated, interpolated, or edge pixels
# using PixelFlags. For matchOptimisticB set this to False to recover
# previous matcher selector behavior.
config.astrometry.sourceSelector['matcher'].excludePixelFlags=False

# specify the minimum psfFlux for good Psf Candidates. Unit=instrument
# flux
config.astrometry.sourceSelector['objectSize'].fluxMin=100.0

# Minimum number of matched pairs; see also minFracMatchedPairs.
# config.astrometry.matcher.minMatchedPairs=10

# the maximum match distance is set to mean_match_distance +
# matchDistanceSigma*std_dev_match_distance; ignored if not fitting a
# WCS
# config.astrometry.matcher.numRefRequireConsensus=2000

# the maximum match distance is set to mean_match_distance +
# matchDistanceSigma*std_dev_match_distance; ignored if not fitting a
# WCS
# config.astrometry.matchDistanceSigma=2.0


config.photoCal.applyColorTerms = False
config.photoCal.photoCatName = ref_cat

# Matching radius in arcsec; keep the VIRCAM override.
config.photoCal.match.matchRadius = 1.0


# Prevent spurious detections in vignetting areas
# config.detection.thresholdType = 'stdev'
# config.detection.thresholdValue = 10.0  # default=5.


config.measurement.load(os.path.join(obsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(obsConfigDir, "kron.py"))
config.measurement.load(os.path.join(obsConfigDir, "hsm.py"))

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.2

# Exposure summary stats
config.computeSummaryStats.load(os.path.join(obsConfigDir, "computeExposureSummaryStats.py"))

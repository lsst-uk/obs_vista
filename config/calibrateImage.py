import math
import os.path

from lsst.meas.algorithms import ColorLimit

config_dir = os.path.dirname(__file__)


# Install a simple Gaussian PSF in the exposure
config.install_simple_psf.fwhm = 1.5*2.0*math.sqrt(2.0*math.log(2.0))



# ObjectSizeStarSelectorTask configurations
# -----------------------------------------

# Reduce contraints to try to get more psf candidates.
config.psf_measure_psf.starSelector['objectSize'].doFluxLimit = True # Default: False
# Flux value/mag relation depends on exposure time.
config.psf_measure_psf.starSelector['objectSize'].fluxMin = 100.0 # Default: 12500.0

# The "nSigmaClip" refers the threshold for excluding outliers when
# selecting stars for PSF determination. Increasing this value allows
# objects that deviate more from the median (by more than 2 sigma) to
# still be included in the selection.
config.psf_measure_psf.starSelector['objectSize'].nSigmaClip = 5.0 # Default: 2.0

# Apply signal-to-noise (i.e. flux/fluxErr) limit to Psf Candidate selection.
config.psf_measure_psf.starSelector['objectSize'].doSignalToNoiseLimit= True
config.psf_measure_psf.starSelector['objectSize'].signalToNoiseMin = 5.0 # Default: 50.0

# Maximum and Minimum width to include in histogram.
config.psf_measure_psf.starSelector['objectSize'].widthMax = 20.0 # Default: 10.0
config.psf_measure_psf.starSelector['objectSize'].widthMin = 0.5 # Default: 0.9

# Standard deviation of width allowed to be interpreted as good
# stars. Increasing the standard deviation allows for more variation
# in star width, meaning the selection criteria become less strict.
config.psf_measure_psf.starSelector['objectSize'].widthStdAllowed = 5.0 # Default: 0.15


# Reduce the minimum SNR for stars used in aperture correction.
config.measure_aperture_correction.sourceSelector["science"].signalToNoise.minimum = 5.0


# Rejection threshold (stdev) for candidates based on spatial fit.
config.psf_measure_psf.psfDeterminer['psfex'].spatialReject=1.0  # Default: 3.0

# Specifies the meaning of thresholdValue.
config.psf_detection.thresholdType = "stdev"

# Threshold for detecting footprints; exact meaning and units depend on thresholdType.
config.psf_detection.thresholdValue=1.0


# Minimum allowed signal-to-noise ratio for sources used for matching
config.psf_measure_psf.starSelector['matcher'].minSnr = 5.0  # Default: 40.0
config.psf_measure_psf.starSelector['astrometry'].minSnr=5.0

# Exclude objects that have saturated, interpolated, or edge pixels using PixelFlags
config.psf_measure_psf.starSelector['matcher'].excludePixelFlags = False # Default: True


# Use PS1 for both astrometry and photometry.
config.connections.astrometry_ref_cat = "ps1_pv3_3pi_20170110_vista"
config.connections.photometry_ref_cat = "ps1_pv3_3pi_20170110_vista"
config.astrometry_ref_loader.load(os.path.join(config_dir, "filterMap.py"))

# Use the filterMap instead of the "any" filter (as is used for Gaia).
config.astrometry_ref_loader.anyFilterMapsToThis = None
config.photometry_ref_loader.load(os.path.join(config_dir, "filterMap.py"))

# Use colorterms for photometric calibration, with color limits on the refcat.
config.photometry.applyColorTerms = True
config.photometry.photoCatName = "ps1_pv3_3pi_20170110_vista"

#colors = config.photometry.match.referenceSelection.colorLimits
#colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
#colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photometry.colorterms.load(os.path.join(config_dir, "colorterms.py"))

# Exposure summary stats
config.compute_summary_stats.load(os.path.join(config_dir, "computeExposureSummaryStats.py"))

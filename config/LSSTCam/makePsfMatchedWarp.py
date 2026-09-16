"""VIRCAM overrides for MakePsfMatchedWarpTask."""

# Target PSF FWHM of 1.8 arcsec on the LSST skymap
# (0.2 arcsec/pixel).
config.modelPsf.defaultFwhm = 9.0

# Larger kernel to accommodate broad PSF matching.
config.psfMatch.kernel['AL'].kernelSize = 41

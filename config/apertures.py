# Set up aperture photometry
# 'config' should be a SourceMeasurementConfig

config.plugins.names |= ["base_CircularApertureFlux"]
# Roughly (1.0, 1.5, 2.0, 3.0, 4.0, 5.7, 8.4, 11.8, 16.8, 23.5 arcsec) in diameter: 2**(0.5*i)
# (assuming plate scale of 0.168 arcsec pixels)
config.plugins["base_CircularApertureFlux"].radii = [3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]

# Use a large aperture to be independent of seeing in calibration
# This config matches obs_subaru, to facilitate 1:1 comparisons between
# VIRCAM and HSC.
config.plugins["base_CircularApertureFlux"].maxSincRadius = 12.0

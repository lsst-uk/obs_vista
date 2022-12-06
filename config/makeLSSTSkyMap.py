# Taken from https://github.com/lsst/obs_lsst/blob/main/config/makeSkyMap.py
# This may change
config.name = "LSST"
config.skyMap.name = "rings"
config.skyMap["rings"].numRings = 120
config.skyMap["rings"].projection = "TAN"
config.skyMap["rings"].tractOverlap = 1.0/60 # Overlap between tracts (degrees)
config.skyMap["rings"].pixelScale = 0.2

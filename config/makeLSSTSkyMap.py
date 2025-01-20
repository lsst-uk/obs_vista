config.name = "lsst_cells_v1"
config.skyMap.name = "rings"
config.skyMap["rings"].numRings = 120
config.skyMap["rings"].projection = "TAN"
config.skyMap["rings"].tractOverlap = 1.0/60
config.skyMap["rings"].pixelScale = 0.2
config.skyMap["rings"].tractBuilder.name = "cells"

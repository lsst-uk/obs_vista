config.name = "lsst_cells_v2"
config.skyMap.name = "rings"
config.skyMap["rings"].numRings = 120
config.skyMap["rings"].projection = "TAN"
config.skyMap["rings"].tractOverlap = 1.0/60
config.skyMap["rings"].pixelScale = 0.2
config.skyMap["rings"].tractBuilder.name = "cells"

# Match the DP2 LSSTCam skymap geometry: cellBorder must be 0 so
# legacy CellCoadds have no padding and can be rewritten to CellCoadd.
config.skyMap["rings"].tractBuilder["cells"].cellBorder = 0

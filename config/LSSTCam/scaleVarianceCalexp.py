# Configuration for VIRCAM calexp variance normalization.

config.scaleVariance.maskPlanes = [
    "DETECTED",
    "DETECTED_NEGATIVE",
    "BAD",
    "SAT",
    "NO_DATA",
    "INTRP",
]

config.scaleVariance.background.ignoredPixelMask = [
    "DETECTED",
    "DETECTED_NEGATIVE",
    "BAD",
    "SAT",
    "NO_DATA",
    "INTRP",
]

config.scaleVariance.background.statisticsProperty = "MEANCLIP"
config.scaleVariance.background.binSize = 32
config.scaleVariance.background.algorithm = "AKIMA_SPLINE"
config.scaleVariance.limit = 10.0

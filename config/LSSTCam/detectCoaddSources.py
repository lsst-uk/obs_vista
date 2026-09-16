# Do not empirically rescale the coadd variance.
config.doScaleVariance = False

# Limit dynamic-detection adjustments.
config.detection.minThresholdScaleFactor = 0.5
config.detection.maxThresholdScaleFactor = 1.2
config.detection.minBackgroundTweak = -8.0
config.detection.maxBackgroundTweak = 5.0

# Background estimation.
config.detection.doTempWideBackground = True
config.detection.tempWideBackground.binSize = 128
config.detection.tempWideBackground.useApprox = False

config.detection.reEstimateBackground = True
config.detection.background.binSize = 128
config.detection.background.useApprox = False

# Detection threshold.
config.detection.thresholdType = "stdev"
config.detection.thresholdValue = 4.5

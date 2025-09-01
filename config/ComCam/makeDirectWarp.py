# config.doApplyNewBackground = True

config.warper.warpingKernelName = 'lanczos5'
config.coaddPsf.warpingKernelName = 'lanczos5'

# Added after all calexps being rejected
# Maximum median ellipticity residual
config.select.maxEllipResidual = 0.1 #default 0.007

# Maximum scatter in the size residuals, scaled by the median size
config.select.maxScaledSizeScatter = 0.022


# Based on ComCam config
config.select.maxPsfTraceRadiusDelta = 4.4
config.select.maxPsfApFluxDelta = 1.6
config.select.maxPsfApCorrSigmaScaledDelta = 0.13
config.doApplyFlatBackgroundRatio = True

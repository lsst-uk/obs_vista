# Added after all calexps being rejected
# Maximum median ellipticity residual
config.select.maxEllipResidual=0.1 #default 0.007

# Maximum scatter in the size residuals, scaled by the median size
config.select.maxScaledSizeScatter=1.0 #default 0.009

config.makePsfMatched = True

# Set to True when we have sky background estimate
#config.doApplySkyCorr = True

config.modelPsf.defaultFwhm = 7.7
# config.matchingKernelSize = 29
config.warpAndPsfMatch.psfMatch.kernel["AL"].kernelSize = 29
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardSigGauss = [1.0, 2.0, 4.5]
config.warpAndPsfMatch.warp.warpingKernelName = 'lanczos5'
config.coaddPsf.warpingKernelName = 'lanczos5'

config.doApplyExternalPhotoCalib = False  # This is also done in the HS example. Why?
config.doApplyExternalSkyWcs = False
config.doApplySkyCorr = False
# 'EDGE' removed to avoid cropping stacks
#config.badMaskPlanes=['BAD', 'DETECTED_NEGATIVE', 'NO_DATA']


# Added after all calexps being rejected
# Maximum median ellipticity residual
config.select.maxEllipResidual=0.1 #default 0.007

# Maximum scatter in the size residuals, scaled by the median size
config.select.maxScaledSizeScatter=1.0 #default 0.009
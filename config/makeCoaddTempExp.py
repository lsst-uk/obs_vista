config.doApplyExternalPhotoCalib = False  # This is also done in the HS example. Why?
config.doApplyExternalSkyWcs = False
config.doApplySkyCorr = False
# 'EDGE' removed to avoid cropping stacks
config.badMaskPlanes=['BAD', 'DETECTED', 'DETECTED_NEGATIVE', 'NO_DATA']

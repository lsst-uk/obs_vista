from lsst.pipe.tasks.selectImages import PsfWcsSelectImagesTask

# 100 rows (based on patch width in ComCam)
config.subregionSize = (10000, 100)
config.assembleStaticSkyModel.subregionSize = (10000, 100)

config.doMaskBrightObjects = True
config.removeMaskPlanes.append("CROSSTALK")
config.doNImage = True
config.badMaskPlanes += ["SUSPECT"]

# Set to True when we get transmission curves
config.doAttachTransmissionCurve = True
# Saturation trails are usually oriented east-west, so along rows
config.interpImage.transpose = True
config.coaddPsf.warpingKernelName = "lanczos5"

config.select.retarget(PsfWcsSelectImagesTask)

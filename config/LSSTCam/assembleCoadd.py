from lsst.pipe.tasks.selectImages import PsfWcsSelectImagesTask

# Process the coadd in narrow row strips to control memory use.
config.subregionSize = (10000, 100)
config.assembleStaticSkyModel.subregionSize = (10000, 100)

config.doMaskBrightObjects = True
config.removeMaskPlanes.append("CROSSTALK")
config.doNImage = True
config.badMaskPlanes += ["SUSPECT"]

# VIRCAM inputs currently do not provide transmission curves.
config.doAttachTransmissionCurve = False

config.interpImage.transpose = True
config.coaddPsf.warpingKernelName = "lanczos5"

config.select.retarget(PsfWcsSelectImagesTask)

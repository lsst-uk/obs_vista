'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''

# from lsst.obs.vista import VircamIsrTask
# config.retarget(VircamIsrTask)
config.doVircamConfidence=True
config.updateVircamBBox=True

config.expectWcs = True
# config.doWrite = True
config.doOverscan = False
# config.doAddDistortionModel = False # Broke tests in 20.0.0
config.doLinearize = False  # made false after failing. Should we be doing linearization?
config.doDefect = False

config.doBias = False
config.doDark = False
config.doFlat = False
config.doSaturationInterpolation = False

# Mask saturated pixels? NB: this is totally independent of the interpolation option - this is ONLY setting the bits in the mask. To have them interpolated make sure doSaturationInterpolation=True
config.doSaturation=True

# trim out non-data regions?
config.assembleCcd.doTrim=False


config.doAssembleIsrExposures = True

# Setting this to false leaves the edge pixels in but masks them as edge
#Turning it off seems to break the wcs possibly because it isn't applying the flipping
# Assemble amp-level exposures into a ccd-level exposure?
config.doAssembleCcd=True

# Should we set the level of all BAD patches of the chip to the chip's average value?
config.doSetBadRegions=True

# Interpolate masked pixels?
config.doInterpolate=False
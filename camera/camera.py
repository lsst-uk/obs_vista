import lsst.afw.cameraGeom.cameraConfig

# This simply asserts whether the config class is of the
# right format.
assert type(config) == lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (
    type(config).__module__, type(config).__name__)

# Sets the plate scale in arcsec/mm:
config.plateScale = 16.95    # Calculated from 0.339 arcesc/px and px = 0.02 mm

# This defines the native coordinate system:
# FocalPlane is (x,y) in mm (rather than radians or pixels, for example).
config.transformDict.nativeSys = 'FocalPlane'

# For some reason, it must have "Pupil" defined:
config.transformDict.transforms = {}
config.transformDict.transforms['FieldAngle'] = \
    lsst.afw.geom.transformConfig.TransformConfig()

# coeffs = [0,1] is the default. This is only necessary if you want to convert
# between positions on the focal plane.
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.retarget(
    target=lsst.afw.geom.transformRegistry['radial'])
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.coeffs = [0.0, 1.0]
config.transformDict.transforms['FieldAngle'].transform.name = 'inverted'

# Define the 16 CCDs that comprise VIRCAM.
# TODO: set all 16 after checking we can import with one test ccd
config.detectorList = {}
for i in range(1,16):
    config.detectorList[i] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
    config.detectorList[i].bbox_y0 = 0         # y0 of pixel bounding box
    config.detectorList[i].bbox_y1 = 2048      # y1 of pixel bounding box
    config.detectorList[i].bbox_x1 = 2048      # x1 of pixel bounding box
    config.detectorList[i].bbox_x0 = 0         # x0 of pixel bounding box
    config.detectorList[i].name = str(i)   # Name of detector slot
    config.detectorList[i].pixelSize_x = 0.020  # Pixel size in mm
    config.detectorList[i].pixelSize_y = 0.020
    config.detectorList[i].transformDict.nativeSys = 'Pixels'  # Name of native coordinate system
    # x position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i].refpos_x = 2048
    # y position of the reference point in the detector in pixels in transposed coordinates.
    config.detectorList[i].refpos_y = 2048
    # Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
    config.detectorList[i].detectorType = 0
    # x offset from the origin of the camera in mm in the transposed system.
    config.detectorList[i].offset_x = 0.   # TODO: set value
    config.detectorList[i].offset_y = 0.   # TODO: set value
    config.detectorList[i].yawDeg = 0.0
    config.detectorList[i].rollDeg = 0.0
    config.detectorList[i].pitchDeg = 0.0
    # Serial string associated with this specific detector
    config.detectorList[i].serial = '{}'.format(i)
    # ID of detector slot
    config.detectorList[i].id = i

# Name of this config
# This isn't strictly required for CameraMapper
# but I'm keeping it there as it seems like a good idea:
config.name = 'Vircam'

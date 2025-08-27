# Configuration for background model of the entire focal-plane
# # These are the dimensions in millimeters of the "superpixels" in
# focalplane coordinates over which the sky background is computed.
# See the comments in the
# `lsst.pipe.tasks.background.FocalPlaneBackgroundConfig` class.
# This config matches obs_subaru
config.xSize = 8192 * 0.015  # in mm
config.ySize = 8192 * 0.015  # in mm
config.pixelSize = 0.015  # mm per pixel

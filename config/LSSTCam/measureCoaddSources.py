import os.path

config_dir = os.path.dirname(__file__)

config.measurement.load(os.path.join(config_dir, "apertures.py"))
config.measurement.load(os.path.join(config_dir, "kron.py"))
config.measurement.load(os.path.join(config_dir, "convolvedFluxes.py"))
config.measurement.load(os.path.join(config_dir, "hsm.py"))
config.load(os.path.join(config_dir, "cmodel.py"))

config.measurement.plugins.names |= ["base_InputCount"]

# The joint LSST + VIRCAM processing does not require propagation
# from visit-level source catalogs.
config.doPropagateFlags = False

# DP2 CellCoadds contain no sensor edges, so SENSOR_EDGE
# should not be requested by the PixelFlags measurement plugin.
pixel_flags = config.measurement.plugins["base_PixelFlags"]

pixel_flags.masksFpAnywhere = [
    mask for mask in pixel_flags.masksFpAnywhere
    if mask != "SENSOR_EDGE"
]

pixel_flags.masksFpCenter = [
    mask for mask in pixel_flags.masksFpCenter
    if mask != "SENSOR_EDGE"
]

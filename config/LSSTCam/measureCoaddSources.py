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

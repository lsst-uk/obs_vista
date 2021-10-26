import os.path

from lsst.meas.base import CircularApertureFluxAlgorithm

config.measurement.load(os.path.join(os.path.dirname(__file__), "apertures.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "kron.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "convolvedFluxes.py"))
config.load(os.path.join(os.path.dirname(__file__), "cmodel.py"))

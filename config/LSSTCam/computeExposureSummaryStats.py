import os.path

config_dir = os.path.dirname(__file__)

# VIRCAM-specific fiducial exposure-summary values have not yet
# been defined/validated, so retain the task defaults.
#
# config.load(os.path.join(config_dir, "fiducialPsfSigma.py"))
# config.load(os.path.join(config_dir, "fiducialSkyBackground.py"))
# config.load(os.path.join(config_dir, "fiducialZeroPoint.py"))
# config.load(os.path.join(config_dir, "fiducialMagLim.py"))

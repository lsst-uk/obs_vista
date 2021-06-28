import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import SourceDetectionTask

for sub in (
    "deblendCoaddSources",
    "detectCoaddSources",
    "mergeCoaddDetections",
    "measureCoaddSources",
    "mergeCoaddMeasurements",
        "forcedPhotCoadd"):
    path = os.path.join(getPackageDir("obs_vista"), "config", sub + ".py")
    if os.path.exists(path):
        getattr(config, sub).load(path)

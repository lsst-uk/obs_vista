import os.path

from lsst.utils import getPackageDir

# Always produce these output bands in the Parquet coadd tables, no matter
# what bands are in the input.
config.outputBands = [
    "g", "r", "i", "z", "y", 
    "Z", "Y", "J", "H", "Ks"]

# Use the environment variable to prevent hardcoding of paths
# into quantum graphs.
ObsConfigDir = os.path.dirname(__file__)
config.functorFile = os.path.join(ObsConfigDir.replace('config','policy'), 'Object.yaml')

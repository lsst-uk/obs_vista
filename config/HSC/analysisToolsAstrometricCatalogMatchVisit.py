import os.path
from lsst.pipe.tasks.postprocess import TransformObjectCatalogConfig


#from .connections import PipelineTaskConnections, iterConnections
#from .connectionTypes import Input

ObsConfigDir = os.path.dirname(__file__)

# Reference catalogs
# The following was copied from obs_subaru and manages conflicts
# between gen2 and gen3
config.connections.refCat = "ps1_pv3_3pi_20170110_vista"

# Use PS1/VISTA for both astrometry and photometry.

config.referenceCatalogLoader.refObjLoader.load(os.path.join(ObsConfigDir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia.

config.referenceCatalogLoader.refObjLoader.anyFilterMapsToThis = None

# By default loop over all the same bands that are present in the
# Object Table

objectConfig = TransformObjectCatalogConfig()
objectConfig.load(os.path.join(os.path.dirname(__file__), "transformObjectCatalog.py"))


#config.bands = ['g', 'r', 'i', 'z', 'y', 'z2', 'y2', 'j', 'h', 'ks', 'z2', 'y2', 'j', 'h', 'ks']
#config.filterNames = ['EXT-G', 'EXT-R', 'EXT-I', 'EXT-Z', 'EXT-Y', 'VIRCAM-Z', 'VIRCAM-Y', 'VIRCAM-J', 'VIRCAM-H', 'VIRCAM-Ks', 'Z', 'Y', 'J', 'H', 'K']

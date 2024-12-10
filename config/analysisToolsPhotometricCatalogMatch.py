import os.path

OBS_CONFIG_DIR = os.path.dirname(__file__)

config.connections.refCat = "ps1_pv3_3pi_20170110_vista"

config.referenceCatalogLoader.doApplyColorTerms = True
config.referenceCatalogLoader.colorterms.load(os.path.join(OBS_CONFIG_DIR, "colorterms.py"))
config.referenceCatalogLoader.refObjLoader.load(os.path.join(OBS_CONFIG_DIR, "filterMap.py"))
config.filterNames = ['EXT-G', 'EXT-R', 'EXT-I', 'EXT-Z', 'EXT-Y', 'VIRCAM-Z', 'VIRCAM-Y', 'VIRCAM-J', 'VIRCAM-H', 'VIRCAM-Ks', 'Z', 'Y', 'J', 'H', 'K']

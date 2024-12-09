import os.path

config.measurement.load(os.path.join(os.path.dirname(__file__), "apertures.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "kron.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "convolvedFluxes.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "hsm.py"))
config.load(os.path.join(os.path.dirname(__file__), "cmodel.py"))

# Try to get measurement running before setting up reference catalogues
# config.doMatchSources = True


config.connections.refCat = "ps1_pv3_3pi_20170110_vista"

config.match.refObjLoader.load(os.path.join(os.path.dirname(__file__), "filterMap.py"))

#config.doWriteMatchesDenormalized = True


config.measurement.plugins.names |= ["base_InputCount"]


# This must be switched off to use imported HSC calexps as we do not
# import the exposure src cats Whether to match sources to CCD
# catalogs to propagate flags (to e.g. identify PSF stars)
config.doPropagateFlags = False

# config.doReplaceWithNoise = False #Just to see if this removes 'Quadropole determinant cannot be negative error' doesn't run with it


# config.measurement.plugins.names=['base_GaussianFlux', 'base_LocalPhotoCalib', 'base_Variance',
# 'base_Blendedness',
# 'base_SdssShape', 'base_LocalWcs', 'base_SdssCentroid', 'base_PsfFlux', 'base_CircularApertureFlux', 'base_SkyCoord', 'base_NaiveCentroid', 'base_InputCount', 'base_PixelFlags', 'base_LocalBackground']#config.sfm.doBlendedness=False #config.measurement.undeblended['base_Blendedness'].doOld=False #? stop negative determinant error?

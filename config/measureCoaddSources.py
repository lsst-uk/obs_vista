import os.path

config.measurement.load(os.path.join(os.path.dirname(__file__), "apertures.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "kron.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "convolvedFluxes.py"))
config.measurement.load(os.path.join(os.path.dirname(__file__), "hsm.py"))
config.load(os.path.join(os.path.dirname(__file__), "cmodel.py"))

#Try to get measurement running before setting up reference catalogues
config.doMatchSources=False

#config.match.refObjLoader=None
# Set reference catalog for Gen2. "ps1_pv3_3pi_vist2020"
config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110_vista" #ps1_pv3_3pi_20170110
# Set reference catalog for Gen3.
config.connections.refCat = "ps1_pv3_3pi_20170110_vista" #ps1_pv3_3pi_20170110

config.doPropagateFlags=False #This being true fails due to data ids - the bits I'm using?
#config.doWriteMatchesDenormalized = True

#config.doReplaceWithNoise = False #Just to see if this removes 'Quadropole determinant cannot be negative error' doesn't run with it



#config.measurement.plugins.names=['base_GaussianFlux', 'base_LocalPhotoCalib', 'base_Variance', 
#'base_Blendedness', 
#'base_SdssShape', 'base_LocalWcs', 'base_SdssCentroid', 'base_PsfFlux', 'base_CircularApertureFlux', 'base_SkyCoord', 'base_NaiveCentroid', 'base_InputCount', 'base_PixelFlags', 'base_LocalBackground']#config.sfm.doBlendedness=False #config.measurement.undeblended['base_Blendedness'].doOld=False #? stop negative determinant error?
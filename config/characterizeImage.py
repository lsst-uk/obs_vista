'''
VIRCAM-specific overrides for CharacterizeImageTask
'''

import os.path

ObsConfigDir = os.path.dirname(__file__)

# PSF determination
# These configs match obs_subaru, to facilitate 1:1 comparisons between
# VIRCAM and HSC.
config.measurePsf.reserve.fraction = 0.2

# Detection overrides to keep results the same post DM-39796
config.detection.doTempLocalBackground = False
config.detection.thresholdType = "stdev"
# Reduce contraints to try to get more psf candidates
config.measurePsf.starSelector['objectSize'].doFluxLimit = True
# flux value/mag relation depends on exposure time for given band and stack vs exposure
config.measurePsf.starSelector['objectSize'].fluxMin = 1000.0  # 12500.0 #1000. fine for stacks
#config.measurePsf.starSelector["objectSize"].doSignalToNoiseLimit = False
# specify the minimum signal-to-noise for good Psf Candidates
config.measurePsf.starSelector['objectSize'].signalToNoiseMin = 5.0  # 20.0
# Maximum width to include in histogram
config.measurePsf.starSelector['objectSize'].widthMax = 20.0  # 10.0
# From obs_subaru:
#config.measurePsf.starSelector["objectSize"].widthMin = 0.9
# Standard deviation of width allowed to be interpreted as good stars
config.measurePsf.starSelector['objectSize'].widthStdAllowed = 5.0  # 0.15
# Keep objects within this many sigma of cluster 0's median
config.measurePsf.starSelector['objectSize'].nSigmaClip = 5.0  # 2.0
config.measurePsf.starSelector['astrometry'].minSnr = 5.0  # 10.0
config.measurePsf.starSelector['matcher'].minSnr = 5.0  # 40.0
config.measurePsf.starSelector['matcher'].excludePixelFlags = False



# Activate calibration of measurements: required for aperture corrections
config.load(os.path.join(ObsConfigDir, "cmodel.py"))
config.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.measurement.load(os.path.join(ObsConfigDir, "convolvedFluxes.py"))
config.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))
if "ext_shapeHSM_HsmShapeRegauss" in config.measurement.plugins:
    # no deblending has been done
    config.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = ""

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.168

# Convolved fluxes can fail for small target seeing if the observation seeing
# is larger
if "ext_convolved_ConvolvedFlux" in config.measurement.plugins:
    names = config.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames()
    config.measureApCorr.allowFailure += names

if "ext_gaap_GaapFlux" in config.measurement.plugins:
    names = config.measurement.plugins["ext_gaap_GaapFlux"].getAllGaapResultNames()
    config.measureApCorr.allowFailure += names




# Too many CR pixels error
# Fix by upping this from 10000
# Why is it so high? 2k * 2k = 4 m total pixels. 100*100 bad pixels in a ccd?
# Good PSF peaks are being flagged as CR
config.repair.doCosmicRay = False
config.repair.cosmicray.nCrPixelMax = 10000000
# CRs must be > this many sky-sig above sky
# config.repair.cosmicray.minSigma=40.0 #6.0
# CRs must have > this many DN (== electrons/gain) in initial detection
# config.repair.cosmicray.min_DN=1000.0
# used in condition 3 for CR; see CR.cc code
# config.repair.cosmicray.cond3_fac=2.5
# used in condition 3 for CR; see CR.cc code
# config.repair.cosmicray.cond3_fac2=0.9

# This sets the reference catalog name for Gen2.
# Note that in Gen3, we've stopped pretending (which is what Gen2 does,
# for backwards compatibility) that charImage uses a reference catalog.
#config.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110_vista"

# measureApCorr error?
# example failure: dataId={'dateObs': '2012-11-22', 'visit': 658653, 'filter': 'VISTA-Ks', 'hdu': 9, 'ccdnum': 8, 'ccd': 8}
# RuntimeError: Unable to measure aperture correction for required algorithm 'base_GaussianFlux': only 1 sources, but require at least 2.
# config.calibrate.measurement.undeblended['base_GaussianFlux'].doMeasure=True
# config.measureApCorr.allowFailure = [
#     'base_GaussianFlux',
#     'base_PsfFlux',
#     'base_Blendedness'
# ]  # ??


# Trial and error from obs goto:
#config.detection.minPixels = 20
#config.detection.thresholdValue = 5.0
#config.detection.includeThresholdMultiplier = 20.0
#config.detection.minPixels = 5
# config.detection.doTempLocalBackground=True
#config.detection.tempLocalBackground.binSize = 32
#config.measurePsf.psfDeterminer.name = "pca"
#config.measurePsf.psfDeterminer['pca'].nEigenComponents = 6
# config.measurePsf.psfDeterminer['pca'].spatialOrder = #config.measurePsf.psfDeterminer['pca'].sizeCellX = 100
#config.measurePsf.psfDeterminer['pca'].sizeCellY = 100
#config.measurePsf.psfDeterminer['pca'].reducedChi2ForPsfCandidates = 20.0
#config.measurePsf.psfDeterminer['pca'].spatialReject = 20.0

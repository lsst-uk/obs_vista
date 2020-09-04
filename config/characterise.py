'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''

#Too many CR pixels error
#Fix by upping this from 10000
#Why is it so high? 2k * 2k = 4 m total pixels. 100*100 bad pixels in a ccd?
config.repair.doCosmicRay=False
config.repair.cosmicray.nCrPixelMax=1000000
# CRs must be > this many sky-sig above sky
config.repair.cosmicray.minSigma=40.0 #6.0
# CRs must have > this many DN (== electrons/gain) in initial detection
config.repair.cosmicray.min_DN=1000.0
# used in condition 3 for CR; see CR.cc code
config.repair.cosmicray.cond3_fac=2.5
# used in condition 3 for CR; see CR.cc code
config.repair.cosmicray.cond3_fac2=0.9

#measureApCorr error?
# example failure: dataId={'dateObs': '2012-11-22', 'visit': 658653, 'filter': 'VISTA-Ks', 'hdu': 9, 'ccdnum': 8, 'ccd': 8}
#RuntimeError: Unable to measure aperture correction for required algorithm 'base_GaussianFlux': only 1 sources, but require at least 2.
#config.calibrate.measurement.undeblended['base_GaussianFlux'].doMeasure=True
config.measureApCorr.allowFailure=[
    'base_GaussianFlux', 
    'base_PsfFlux', 
    'base_Blendedness'
] #??


#Reduce contraints to try to get more psf candidates
#flux value/mag relation depends on exposure time for given band and stack vs exposure
config.measurePsf.starSelector['objectSize'].fluxMin=50.0 #12500.0 #1000. fine for stacks
config.measurePsf.starSelector['objectSize'].signalToNoiseMin=5.0 #20.0
config.measurePsf.starSelector['objectSize'].widthMax=20.0 #10.0
config.measurePsf.starSelector['objectSize'].widthStdAllowed=10.0 #0.15
config.measurePsf.starSelector['objectSize'].nSigmaClip=5.0 #2.0
config.measurePsf.starSelector['astrometry'].minSnr=5.0 #10.0
config.measurePsf.starSelector['matcher'].minSnr=5.0 #40.0
config.measurePsf.starSelector['matcher'].excludePixelFlags=False
config.measurePsf.starSelector['objectSize'].badFlags=[
    #'base_PixelFlags_flag_edge', 
    #'base_PixelFlags_flag_interpolatedCenter', 
    #'base_PixelFlags_flag_saturatedCenter', 
    #'base_PixelFlags_flag_crCenter', 
    #'base_PixelFlags_flag_bad', 
    #'base_PixelFlags_flag_interpolated'
]
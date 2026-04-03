config.detection.doTempWideBackground = True
config.detection.tempWideBackground.binSize = 128
config.detection.tempWideBackground.useApprox = False
config.detection.reEstimateBackground = True
config.detection.background.binSize = 128
config.detection.background.useApprox = False


# Not enough detections?
# https://community.lsst.org/t/detectcoaddsource-detection-threshold-on-noisy-background-data/3050
#from lsst.meas.algorithms import SourceDetectionTask
#config.detection.retarget(SourceDetectionTask) #use simpler detection algorithm
config.detection.thresholdType='stdev' #default='pixel_stdev'
config.detection.thresholdValue=10.0 #default=5. 5 leads to large detected areas possibly due to variance scaling

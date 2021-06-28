# Not enough detections?
# https://community.lsst.org/t/detectcoaddsource-detection-threshold-on-noisy-background-data/3050
#from lsst.meas.algorithms import SourceDetectionTask
# config.detection.retarget(SourceDetectionTask) #use simpler detection algorithm
config.detection.thresholdType = 'stdev'  # default=stdev
config.detection.thresholdValue = 5.0  # default=5.

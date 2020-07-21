'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''
config.doWrite = False
config.doOverscan = False
# config.doAddDistortionModel = False # Broke tests in 20.0.0
config.doLinearize=False
config.doDefect = False
config.doAssembleIsrExposures = False
config.doBias = False
config.doDark = False
config.doFlat = False
config.doSaturationInterpolation = False
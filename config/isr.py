'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''

config.expectWcs = True
# config.doWrite = True
config.doOverscan = False
# config.doAddDistortionModel = False # Broke tests in 20.0.0
config.doLinearize = False  # made false after failing. Should we be doing linearization?
config.doDefect = False
config.doAssembleIsrExposures = False
config.doBias = False
config.doDark = False
config.doFlat = False
config.doSaturationInterpolation = False


# trim out non-data regions?
config.assembleCcd.doTrim=False

# Setting this to false leaves the edge pixels in but masks them as edge
# Assemble amp-level exposures into a ccd-level exposure?
config.doAssembleCcd=False
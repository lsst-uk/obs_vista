'''
This describes the Butler generation 2 metadata to be read from fits headers and used
to populate the exposure registry.

In the third generation Butler this is superseded by the translators but is still used
for converting the repository.

In general we are taking the minimal metadata to enable processing runs.
'''
from lsst.obs.vista.ingest import VistaParseTask
config.parse.retarget(VistaParseTask)

# Metadata that can be read directly from the header
config.parse.translation = {
    'expTime': "EXPTIME",  
    'visit': "ESO DET EXP NO",
   # 'ndit': "HIERARCH ESO DET NDIT",
}

# Metadata requiring 'translation'
config.parse.translators = {
    'filter': 'translateFilter',  
    'dateObs': 'translateDate',
    'taiObs': 'translateTai',
    'mjd': 'translateJd',
    'ccd': 'translateCcd',
    'ccdnum': 'translateCcd',
    'numObs': 'translateNumObs',
    'dataType': 'translateDataType',
 }

config.parse.extnames = [
    'DET1.CHIP1',
    'DET1.CHIP2',
    'DET1.CHIP3',
    'DET1.CHIP4',
    'DET1.CHIP5',
    'DET1.CHIP6',
    'DET1.CHIP7',
    'DET1.CHIP8',
    'DET1.CHIP9',
    'DET1.CHIP10',
    'DET1.CHIP11',
    'DET1.CHIP12',
    'DET1.CHIP13',
    'DET1.CHIP14',
    'DET1.CHIP15',
    'DET1.CHIP16',
]

config.register.visit = ['visit', 'filter', 'dateObs', 'taiObs', 'numObs', 'dataType']
config.register.unique = ['visit', 'ccdnum', 'dataType'] 
config.register.columns = {
    'visit': 'int',
    'numObs': 'text',
    'ccd': 'int',
    'ccdnum': 'int',
    'hdu':'int',
    'filter': 'text',
    'dataType': 'text',
    'expTime': 'double',
    'dateObs': 'text',
    'taiObs': 'text',
    'mjd': 'int',
  #  'ndit': 'int',
}

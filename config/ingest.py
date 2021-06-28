'''
There is a default parse task included with the LSST stack, however it may not
be suited to translate the data in your image headers. Often you'll need to
write your own translator that suited to the data formats in your image header and load it into the stack.

Vista's translators are  saved in:
obs_vista/python/lsst/obs/vista/ingest.py

To load them into the stack, we first import them, then retarget them. 
'''
from lsst.obs.vista.ingest import VistaParseTask
config.parse.retarget(VistaParseTask)
#from lsst.obs.vista.ingest import VistaRawIngestTask
# config.raws.retarget(VistaRawIngestTask)

# The following grabs data from the image headers that don't need parsing (i.e., translating). Header keywords are on the right, stack keywords on the left:
config.parse.translation = {'expTime': "EXPTIME",  # Nothing can go direct
                            'visit': "ESO DET EXP NO",
                            # Is exposure number visit number?
                            # 'dataType': "XTENSION",
                            # 'dateObs':'DATE-OBS',
                            # 'taiObs':'DATE-OBS',
                            }

# These are the data that need to be parsed (translated)
config.parse.translators = {'filter': 'translateFilter',  # 'FILTER'
                            'dateObs': 'translateDate',
                            'taiObs': 'translateTai',
                            'mjd': 'translateJd',
                            'ccd': 'translateCcd',
                            'ccdnum': 'translateCcd',
                            'numObs': 'translateNumObs',
                            'dataType': 'translateDataType',
                            # 'hdu':'translateCcd',
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
    'DET1.CHIP16']

config.register.visit = ['visit', 'filter', 'dateObs', 'taiObs', 'numObs', 'dataType']
config.register.unique = ['visit', 'ccdnum', 'dataType']  # removed ,'ccd'
config.register.columns = {'visit': 'int',
                           'numObs': 'text',
                           'ccd': 'int',
                           'ccdnum': 'int',
                           # 'hdu':'int',#copying from obs_decam
                           # 'instcal': 'text',
                           'filter': 'text',
                           'dataType': 'text',
                           'expTime': 'double',
                           'dateObs': 'text',
                           'taiObs': 'text',
                           'mjd': 'int'
                           }

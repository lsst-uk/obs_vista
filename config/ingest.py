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

#The following grabs data from the image headers that don't need parsing (i.e., translating). Header keywords are on the right, stack keywords on the left:
config.parse.translation = { 'expTime': "EXPTIME",       #Nothing can go direct
                            'visit':    "ESO DET EXP NO",#Is exposure number visit number?
                            'dataType': "XTENSION"
                           }

#These are the data that need to be parsed (translated)
config.parse.translators = {'filter': 'translateFilter', # 'FILTER'
                            'dateObs':'translateDate',
                            'taiObs':'translateDate',
                            'mjd':'translateJd',
                            'ccd':'translateCcd', 
                            'ccdnum':'translateCcd',
                            }
                            
config.register.visit = ['visit', 'filter','dateObs','taiObs']
config.register.unique = ['visit', 'ccd', 'filter'] #removed ,'ccd'
config.register.columns = {'visit':'int',
                           'ccd':'int',
                           'ccdnum':'int',
                           #'hdu':'int',#copying from obs_decam
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                           'mjd':'int'
                           }

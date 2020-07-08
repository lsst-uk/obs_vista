'''
There is a default parse task included with the LSST stack, however it may not
be suited to translate the data in your image headers. Often you'll need to
write your own translator that suited to the data formats in your image header and load it into the stack.

Necam's translators are  saved in:
obs_necam/python/lsst/obs/necam/ingest.py

To load them into the stack, we first import them, then retarget them. 
'''
from lsst.obs.necam.ingest import NecamParseTask
config.parse.retarget(NecamParseTask)

#The following grabs data from the image headers that don't need parsing (i.e., translating). Header keywords are on the right, stack keywords on the left:
config.parse.translation = {'dataType':'IMGTYPE',
                            'filter':'FILTER'
                           }

#These are the data that need to be parsed (translated)
config.parse.translators = {'dateObs':'translateDate',
                            'taiObs':'translateDate',
                            'expTime':'translateExpTime',
                            'visit':'translateVisit',
                            'ccd':'translateCcd'}
                            
config.register.visit = ['visit', 'ccd', 'filter','dateObs','taiObs']
config.register.unique = ['visit', 'ccd', 'filter']
config.register.columns = {'visit':'int',
                           'ccd':'int',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text'
                           }

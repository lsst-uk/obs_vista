from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time
    
class NecamParseTask(ParseTask):

    '''
    [From https://github.com/lsst/obs_lsst/blob/f0c4ae506e8e0a85789aebdd970d7e704c9c6e24/
    python/lsst/obs/lsst/ingest.py#L54]:
    All translator methods receive the header metadata [here via "md"] and should return the appropriate value, or None if the value cannot be determined. 
    '''

    def translateDate(self, md):
        '''
        As an example, this method takes the date in the header of the fits file, which is in the format yyyymmdd, and converts it into yyyy-mm-dd format. This isn't strictly necessary, but it's a good example of what a translate script can be used to do.
        '''
        date = md.get("DATE-OBS")
        date = [date[0:4], date[4:6], date[6:]]
        date = '-'.join(date)
        t = Time(date, format='iso', out_subfmt='date').iso
                
        return t
     
    def translateVisit(self, md):
        '''
        Header information is extracted as string, but "visit" is more suited to integer.
        '''
        return int(md.get("RUN")) 
                    
    def translateCcd(self, md):
        '''
        Header information is extracted as string, but "ccd" is more suited to integer.
        '''
        return int(md.get("INSTRUME"))

    def translateExpTime(self, md):
        '''
        Header information is extracted as string, but "expTime" is more suited to float.
        '''
        return float(md.get("EXPTIME"))  
                

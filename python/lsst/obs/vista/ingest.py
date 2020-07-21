from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time
    
class VistaParseTask(ParseTask):

    '''
    [From https://github.com/lsst/obs_lsst/blob/f0c4ae506e8e0a85789aebdd970d7e704c9c6e24/
    python/lsst/obs/lsst/ingest.py#L54]:
    All translator methods receive the header metadata [here via "md"] and should return the appropriate value, or None if the value cannot be determined.
    
    How does it deal with extensions?
    
    Here we define the functions required to translate the VISTA metadata into the 
    standard required by the LSST stack. It will work with the header keys defined in 
    config/ingest.py
    '''
    def translateDataType(self, md):
        '''Convert dtype header
        
        What is data type? Science vs flat or float vs int arrays?
        '''
        return md.get("XTENSION")
    
    def translateFilter(self, md):
        '''Takes VISTA filter name and converts it
        
        '''
        #Find a better way to get the filter - access to top level header?
        #e.g. turn 'Done with sky_20180911_266_Y.fit[1]' to 'Y'
        return 'VISTA-'+md.get("SKYSUB")[-8:-7]

    def translateDate(self, md):
        '''
        This strips everything apart form yyyy-mm-dd
        '''
        date = md.get("DATE-OBS")
        date = date[0:10]
        
        t = Time(date, format='iso', out_subfmt='date').iso
                
        return t
     
                    
    def translateCcd(self, md):
        '''
        Header information is extracted as string, but "ccd" is more suited to integer.
        
        This seems to give access to the extensions directly. Does this need to return 
        the form of CCD name used in camera?
        '''
        #take e.g. 'DET1.CHIP12' and return the integer 11 (we use 0 indexing)
        #This seems to be just taking the first extension
        #ccd = int(md.get("EXTNAME")[9:]) - 1
        ccd = md.get('ESO DET CHIP NO') -1
        return ccd

                

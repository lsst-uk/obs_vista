#from lsst.afw.geom import degrees  # Failed in 20.0.0
from lsst.geom import degrees #Many basic astro classes moved from afw.geom to geom
from lsst.afw.coord import Observatory
from lsst.obs.base import MakeRawVisitInfo

__all__ = ["MakeVircamRawVisitInfo"]

class MakeVircamRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a VISTA image
    """
    observatory = Observatory(-24.62*degrees, 70.4*degrees, 2518)  # long, lat, elev

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata
        @param[in,out] md metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict a dict of arguments
        
        While a Make<>RawVisitInfo file is mandatory for processCcd.py to run, it isn't mandatory for it to actually do anything. Hence this one simply contains a pass statement.

        However, it's recommended that you at least include the exposure time from the image header and observatory information (for the latter, remember to edit and uncomment the "observatory" variable above.) 
        """
        #Uncommented these
        argDict["exposureTime"] = self.popFloat(md, 'EXPTIME')
        argDict["observatory"] = self.observatory
        #argDict["ccd"] = self.popFloat(md, 'CCDNUM')
        startDate = self.popIsoDate(md, "DATE-OBS")
        argDict["date"] = self.offsetDate(startDate, 0.5*argDict["exposureTime"])
    
    def getDateAvg(self, md, exposureTime):
        """Return date at the middle of the exposure
        @param[in,out] md  FITS metadata; changed in place
        @param[in] exposureTime  exposure time in sec
        """
        dateObs = self.popIsoDate(md, "DATE-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)



      
        
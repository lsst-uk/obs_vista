from __future__ import absolute_import, division, print_function

import os

from lsst.daf.persistence import ButlerLocation, Policy
from lsst.obs.base import CameraMapper
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from .makeVistaRawVisitInfo import MakeVistaRawVisitInfo

class VistaMapper(CameraMapper):
    packageName = 'obs_vista'
    
    # A rawVisitInfoClass is required by processCcd.py
    MakeRawVisitInfoClass = MakeVistaRawVisitInfo

    def __init__(self, inputPolicy=None, **kwargs):

        #Declare the policy file...
        policyFile = Policy.defaultPolicyFile(
            self.packageName, "VistaMapper.yaml", "policy")
        policy = Policy(policyFile)
        #...and add it to the mapper:
        super(VistaMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        ###Defining your filter set###
        #Create a python dict of filters:
        self.filters = {}
 
        #Define your set of filters; you can have as many filters as you like...  
        afwImageUtils.defineFilter(name='Clear',  lambdaEff=535.5, alias=['Clear'])
        
        #...add them to your filter dict...
        self.filters['Clear'] = afwImage.Filter('Clear').getCanonicalName()

        #...and set your default filter.
        self.defaultFilterName = 'Clear'
        ##############################

    def _computeCcdExposureId(self, dataId):
        '''
        Every exposure needs a unique ID.
        Here, I construct a unique ID by multiplying the visit number by
        64 to accomodate that we may have up to 64 CCDs exposed for every visit.
        processCcd.py will fail with a NotImplementedError() without this.
        ''' 
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        visit = int(visit)
        ccd = int(ccd)

        return visit*64 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack that it needs to refer to the above _computeCcdExposureId function.
        processCcd.py will fail with an AttributeError without this.
        '''
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack how many bits to use for the ExposureId. Here I'm say that the ccd ID takes up to 6 bits (2**6=64), and I can have up to 16,777,216 (=2**24) visits in my survey.
        processCcd.py will fail with an AttributeError without this.
        '''
        return 24+6

    def _extractDetectorName(self, dataId):
        '''
        Every detector needs a name.
        Here, I simply use the ccd ID number extracted from the header and recorded via the ingest process.
        processCcd.py will fail with a NotImplementedError() without this.
        ''' 
        return int("%(ccd)d" % dataId)
        
    #def map_linearizer(self, dataId, write=False):
    #    """Map a linearizer.
    #    
    #    This was copied from obs_subaru to fix an error requiring it
    #    What does it do?
    #    
    #    Linearization is part of the instrument signature removal.
    #    
    #    It can be disabled. Should we be doing it for VISTA?
    #    https://community.lsst.org/t/correcting-non-linearity/816
    #    """
    #    actualId = self._transformId(dataId)
    #    return ButlerLocation(
    #        pythonType="lsst.ip.isr.LinearizeSquared",
    #        cppType="Config",
    #        storageName="PickleStorage",
    #        locationList="ignored",
    #        dataId=actualId,
    #        mapper=self,
    #        storage=self.rootStorage)
   
   
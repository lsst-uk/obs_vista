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
        afwImageUtils.defineFilter(name="VISTA-z",lambdaEff=8762.4, alias=['VISTA-z'])
        afwImageUtils.defineFilter(name="VISTA-Y",lambdaEff=10184.2, alias=['VISTA-Y'])
        afwImageUtils.defineFilter(name="VISTA-J",lambdaEff=12464.4, alias=['VISTA-J'])
        afwImageUtils.defineFilter(name="VISTA-H",lambdaEff=16310.0, alias=['VISTA-H'])
        afwImageUtils.defineFilter(name="VISTA-Ks", lambdaEff=21336.6, alias=['VISTA-Ks'])
        
        #...add them to your filter dict...
        self.filters['Clear'] = afwImage.Filter('Clear').getCanonicalName()
        self.filters['VISTA-z'] = afwImage.Filter('VISTA-z').getCanonicalName()
        self.filters['VISTA-Y'] = afwImage.Filter('VISTA-Y').getCanonicalName()
        self.filters['VISTA-J'] = afwImage.Filter('VISTA-J').getCanonicalName()
        self.filters['VISTA-H'] = afwImage.Filter('VISTA-H').getCanonicalName()
        self.filters['VISTA-Ks'] = afwImage.Filter('VISTA-Ks').getCanonicalName()
        

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
        
        
    def _computeCoaddExposureId(self, dataId):
        '''
        Here I'm saying: 
           - we've got up to 1024 (2**10) tracts;
           - we've got up to 64 (2**6) patches in each dimension
        Currently, I'm not incorporating filter information.
        The remaining 64-22 = 42 bits are left for source numbers
        '''
        nbit_tract = 10
        nbit_patch = 6
        tract = int(dataId['tract'])

        patchX, patchY = [int(patch) for patch in dataId['patch'].split(',')]
        oid = (((tract << nbit_patch) + patchX) << nbit_patch) + patchY
        
        return oid

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        #Up to 1024 (2**10) tracts each containing up to 64x64 (2**6x2**6) patches
        return 10+6+6 

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
         return 10+6+6

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)
        

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
   
   
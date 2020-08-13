from __future__ import absolute_import, division, print_function

import os

from lsst.daf.persistence import ButlerLocation, Policy
from lsst.obs.base import CameraMapper
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from .makeVistaRawVisitInfo import MakeVistaRawVisitInfo
from ._instrument import VISTA

class VistaMapper(CameraMapper):
    packageName = 'obs_vista'
    _gen3instrument = VISTA
    
    # A rawVisitInfoClass is required by processCcd.py
    MakeRawVisitInfoClass = MakeVistaRawVisitInfo
    
    detectorNames = {
    0:'DET1.CHIP1',
    1:'DET1.CHIP2',
    2:'DET1.CHIP3',
    3:'DET1.CHIP4',
    4:'DET1.CHIP5',
    5:'DET1.CHIP6',
    6:'DET1.CHIP7',
    7:'DET1.CHIP8',
    8:'DET1.CHIP9',
    9:'DET1.CHIP10',
    10:'DET1.CHIP11',
    11:'DET1.CHIP12',
    12:'DET1.CHIP13',
    13:'DET1.CHIP14',
    14:'DET1.CHIP15',
    15:'DET1.CHIP16'}

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
        
        
        
        for datasetType in ("raw", "instcal"): #, "stack", "tile"):
            self.mappings[datasetType].keyDict.update({'ccdnum': int})
            self.mappings[datasetType].keyDict.update({'ccd': int})
            
        # The number of bits allocated for fields in object IDs
        # TODO: Understand how these were set by obs_decam
        VistaMapper._nbit_tract = 16
        VistaMapper._nbit_patch = 5
        VistaMapper._nbit_filter = 4
        VistaMapper._nbit_id = 64 - (VistaMapper._nbit_tract
                                     + 2*VistaMapper._nbit_patch
                                     + VistaMapper._nbit_filter)
        
    def _extractDetectorName(self, dataId):
        copyId = self._transformId(dataId)
        try:
            return VistaMapper.detectorNames[copyId['ccdnum']]
        except KeyError:
            raise RuntimeError("No name found for dataId: %s"%(dataId))
    
    def _transformId(self, dataId):
        copyId = CameraMapper._transformId(self, dataId)
        if "ccd" in copyId:
            copyId.setdefault("ccdnum", copyId["ccd"])
        return copyId

    def _computeCcdExposureId(self, dataId):
        '''
        Every exposure needs a unique ID.
        Here, I construct a unique ID by multiplying the visit number by
        64 to accomodate that we may have up to 16 CCDs exposed for every visit.
        processCcd.py will fail with a NotImplementedError() without this.
        ''' 
        
        pathId = self._transformId(dataId)
        #print("DEBUG data id", pathId, dataId)
        visit = pathId['visit']
        ccd = int(pathId['hdu']) - 1
        visit = int(visit)
       

        return visit*16 + ccd 

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack that it needs to refer to the above _computeCcdExposureId function.
        processCcd.py will fail with an AttributeError without this.
        '''
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack how many bits to use for the ExposureId. Here I'm say that the ccd ID takes up to 6 bits (2**6=64), and I can have up to 16,777,216 (=2**24) visits in my survey.
        processCcd.py will fail with an AttributeError without this.
        '''
        return 32 #Set large to avoid 'Exposure ID '34910216' is too large.
        
        
    def _computeCoaddExposureId(self, dataId):
        '''
        Here I'm saying: 
           - we've got up to 1024 (2**10) tracts;
           - we've got up to 64 (2**6) patches in each dimension
        Currently, I'm not incorporating filter information.
        The remaining 64-22 = 42 bits are left for source numbers
        '''
        #nbit_tract = 10
        #nbit_patch = 6
        tract = int(dataId['tract'])

        patchX, patchY = [int(patch) for patch in dataId['patch'].split(',')]
        oid = (
            ((tract << VistaMapper._nbit_patch) + patchX) 
            << VistaMapper._nbit_patch
        ) + patchY
        
        return oid

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        #Up to 1024 (2**10) tracts each containing up to 64x64 (2**6x2**6) patches
        return 64 - VistaMapper._nbit_id#10+6+6 #Set large to avoid 'Exposure ID '34910216' is too large.

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
         return 64 - VistaMapper._nbit_id#10+6+6 #Set large to avoid 'Exposure ID '34910216' is too large.

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)
        

    def _extractDetectorName(self, dataId):
        '''
        Every detector needs a name.
        Here, I simply use the ccd ID number extracted from the header and recorded via the ingest process.
        processCcd.py will fail with a NotImplementedError() without this.
        ''' 
        return int("%(hdu)d" % dataId) - 1
        
        
    def std_raw(self, item, dataId):
        """Standardize a raw dataset by converting it to an Exposure.

        Raw images are MEF files with one HDU for each detector.

        Parameters
        ----------
        item : `lsst.afw.image.DecoratedImage`
            The image read by the butler.
        dataId : data ID
            Data identifier.

        Returns
        -------
        result : `lsst.afw.image.Exposure`
            The standardized Exposure.
        """
        return self._standardizeExposure(self.exposures['raw'], item, dataId,
                                         trimmed=False)
        
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
   
   
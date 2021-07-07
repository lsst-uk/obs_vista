from __future__ import absolute_import, division, print_function

import os, warnings

from lsst.daf.persistence import ButlerLocation, Policy
from lsst.obs.base import CameraMapper
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from .makeVircamRawVisitInfo import MakeVircamRawVisitInfo
from .vircamFilters import VIRCAM_FILTER_DEFINITIONS
from ._instrument import VIRCAM


class VistaMapper(CameraMapper):
    packageName = 'obs_vista'
    _gen3instrument = VIRCAM

    # A rawVisitInfoClass is required by processCcd.py
    MakeRawVisitInfoClass = MakeVircamRawVisitInfo

    detectorNames = {
        0: 'DET1.CHIP1',
        1: 'DET1.CHIP2',
        2: 'DET1.CHIP3',
        3: 'DET1.CHIP4',
        4: 'DET1.CHIP5',
        5: 'DET1.CHIP6',
        6: 'DET1.CHIP7',
        7: 'DET1.CHIP8',
        8: 'DET1.CHIP9',
        9: 'DET1.CHIP10',
        10: 'DET1.CHIP11',
        11: 'DET1.CHIP12',
        12: 'DET1.CHIP13',
        13: 'DET1.CHIP14',
        14: 'DET1.CHIP15',
        15: 'DET1.CHIP16'}

    # Can this replace the filter definitions here in gen 3?
    @classmethod
    def addFilters(cls):
        VIRCAM_FILTER_DEFINITIONS.defineFilters()

    def __init__(self, inputPolicy=None, **kwargs):

        # Declare the policy file...
        policyFile = Policy.defaultPolicyFile(
            self.packageName, "VistaMapper.yaml", "policy")
        policy = Policy(policyFile)
        # ...and add it to the mapper:
        super(VistaMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # Ensure each dataset type of interest knows about the full range of keys available from the registry
        keys = {'visit': int,
                'ccd': int,
                'ccdnum': int,
                'filter': str,
                'dataType': str,
                'expTime': float,
                'dateObs': str,
                'taiObs': str,
                # 'mjd': int,
                # 'field': str,
                # 'survey': str
                }
        for name in ("raw",
                     "postISRCCD",
                     #"instcal",
                     #"confmap",
                     # "calexp", "src", "icSrc", "srcMatch",
                     ):
            self.mappings[name].keyDict.update(keys)

        self.addFilters()

        self.filters = {}
        with warnings.catch_warnings():
            # surpress Filter warnings; we already know this is deprecated
            warnings.simplefilter('ignore', category=FutureWarning)
            for filt in VIRCAM_FILTER_DEFINITIONS:
                self.filters[filt.physical_filter] = afwImage.Filter(filt.physical_filter).getCanonicalName()
        self.defaultFilterName = "unknown"

        # for filt in VISTA_FILTER_DEFINITIONS:
        # self.filters[filt.physical_filter] = afwImage.Filter(filt.physical_filter).getCanonicalName()

        # ...and set your default filter.
        self.defaultFilterName = 'Clear'
        ##############################

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
        '''You need to tell the stack that it needs to refer to the above 
        _computeCcdExposureId function.
        processCcd.py will fail with an AttributeError without this.
        '''
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        '''You need to tell the stack how many bits to use for the ExposureId. Here I'm 
        say that the ccd ID takes up to 6 bits (2**6=64), and I can have up to 16,777,216 
        (=2**24) visits in my survey.
        processCcd.py will fail with an AttributeError without this.
        '''
        return 32  # Set large to avoid 'Exposure ID '34910216' is too large.

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
        print(oid)
        return oid

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        # Up to 1024 (2**10) tracts each containing up to 64x64 (2**6x2**6) patches
        return 64 - VistaMapper._nbit_id  # 10+6+6 #Set large to avoid 'Exposure ID '34910216' is too large.

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
        return 64 - VistaMapper._nbit_id  # 10+6+6 #Set large to avoid 'Exposure ID '34910216' is too large.

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId)

    def _extractDetectorName(self, dataId):
        '''
        Every detector needs a name.
        Here, I simply use the ccd ID number extracted from the header and recorded via 
        the ingest process.
        processCcd.py will fail with a NotImplementedError() without this.
        '''
        return int("%(hdu)d" % dataId)

    def translate_confmap(self, confmap):
        confArr = confmap.getArray()

        idxUndefWeight = np.where(confArr <= 0)
        # Reassign weights to be finite but small:
        confArr[idxUndefWeight] = min(1e-14, np.min(confArr[np.where(confArr > 0)]))
        # convert percentages
        confim = afwImage.ImageF(confim/100.)
        return confim

    def bypass_instcal(self, datasetType, pythonType, butlerLocation, dataId):
        # Workaround until I can access the butler
        instcalMap = self.map_instcal(dataId)
        dqmaskMap = self.map_dqmask(dataId)
        wtmapMap = self.map_wtmap(dataId)
        instcalType = getattr(afwImage, instcalMap.getPythonType().split(".")[-1])
        dqmaskType = getattr(afwImage, dqmaskMap.getPythonType().split(".")[-1])
        wtmapType = getattr(afwImage, wtmapMap.getPythonType().split(".")[-1])
        instcal = instcalType(instcalMap.getLocationsWithRoot()[0])
        dqmask = dqmaskType(dqmaskMap.getLocationsWithRoot()[0])
        wtmap = wtmapType(wtmapMap.getLocationsWithRoot()[0])

        mask = self.translate_dqmask(dqmask)
        variance = self.translate_confmap(wtmap)

        mi = afwImage.MaskedImageF(afwImage.ImageF(instcal.getImage()), mask, variance)
        md = readMetadata(instcalMap.getLocationsWithRoot()[0])
        fix_header(md, translator_class=DecamTranslator)
        wcs = makeSkyWcs(md, strip=True)
        exp = afwImage.ExposureF(mi, wcs)

        exp.setPhotoCalib(afwImage.makePhotoCalibFromCalibZeroPoint(10**(0.4 * md.getScalar("MAGZERO")), 0))
        visitInfo = self.makeRawVisitInfo(md=md)
        exp.getInfo().setVisitInfo(visitInfo)

        for kw in ('LTV1', 'LTV2'):
            md.remove(kw)

        exp.setMetadata(md)
        return exp

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

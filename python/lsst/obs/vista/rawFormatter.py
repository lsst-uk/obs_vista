
"""Gen3 Butler Formatters for Vista raw data.
"""


import lsst.afw.fits
import lsst.afw.image
import lsst.log
from lsst.obs.base import FitsRawFormatterBase
from lsst.obs.base.utils import InitialSkyWcsError
from lsst.afw.image import ImageU, bboxFromMetadata
from lsst.afw.geom import makeSkyWcs, makeFlippedWcs
from lsst.afw.math import flipImage
from lsst.geom import Point2D

import astro_metadata_translator
from astro_metadata_translator import fix_header, merge_headers

import logging
log = logging.getLogger("fitsRawFormatter")

from ._instrument import VIRCAM
from .vircamFilters import VIRCAM_FILTER_DEFINITIONS
from .translators import VircamTranslator


__all__ = ("VircamRawFormatter",)


# The mapping of detector id to HDU in raw files for.
# I am trying to move to retain 1 indexing
# We try this first before scaning the HDUs manually.
detector_to_hdu = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
}


class VircamRawFormatter(FitsRawFormatterBase):
    """Gen 3 Butler Formatters for VIRCAM raw data.
    
    This is built on examples from obs_decam, obs_subaru, and obs_necam
    
    """

    
    translatorClass = VircamTranslator
    filterDefinitions = VIRCAM_FILTER_DEFINITIONS
    
    #This is set in base class as False
    wcsFlipX = True
    
    FLIP_LR = False
    FLIP_TB = False

    def getDetector(self, id):
        return VIRCAM().getCamera()[id]
        
    def makeWcs(self, visitInfo, detector):
        """Create a SkyWcs from information about the exposure.
        Overide the default which uses visit info
        Return the metadata-based SkyWcs (always created, so that
        the relevant metadata keywords are stripped).
        
        Is geometry based WCS superior?
        
        Parameters
        ----------
        visitInfo : `~lsst.afw.image.VisitInfo`
            The information about the telescope boresight and camera
            orientation angle for this exposure.
        detector : `~lsst.afw.cameraGeom.Detector`
            The detector used to acquire this exposure.
        Returns
        -------
        skyWcs : `~lsst.afw.geom.SkyWcs`
            Reversible mapping from pixel coordinates to sky coordinates.
        Raises
        ------
        InitialSkyWcsError
            Raised if there is an error generating the SkyWcs, chained from the
            lower-level exception if available.
        """
        #Setting this to True improves the WCS but is very slow due to downloading objs
        useMetadataWcs=False
        if not self.isOnSky():
            # This is not an on-sky observation
            return None

        skyWcs = self._createSkyWcsFromMetadata()

        if useMetadataWcs:
            msg = "VIRCAM camera geom not used. Defaulting to metadata-based SkyWcs."
            log.warning(msg)
            if skyWcs is None:
                raise InitialSkyWcsError("Failed to create both metadata and boresight-based SkyWcs."
                                         "See warnings in log messages for details.")
            return skyWcs
        else:
            return self.makeRawSkyWcsFromBoresight(visitInfo.getBoresightRaDec(),
                                               visitInfo.getBoresightRotAngle(),
                                               detector)
                                               
#     @classmethod
#     def makeRawSkyWcsFromBoresight(cls, boresight, orientation, detector):
#         """Class method to make a raw sky WCS from boresight and detector.
#         Parameters
#         ----------
#         boresight : `lsst.geom.SpherePoint`
#             The ICRS boresight RA/Dec
#         orientation : `lsst.geom.Angle`
#             The rotation angle of the focal plane on the sky.
#         detector : `lsst.afw.cameraGeom.Detector`
#             Where to get the camera geomtry from.
#         Returns
#         -------
#         skyWcs : `~lsst.afw.geom.SkyWcs`
#             Reversible mapping from pixel coordinates to sky coordinates.
#         """
#         #return createInitialSkyWcsFromBoresight(boresight, orientation, detector, flipX=cls.wcsFlipX)
#         return self._createSkyWcsFromMetadata()

    def _scanHdus(self, filename, detectorId):
        """Scan through a file for the HDU containing data from one detector.
        Parameters
        ----------
        filename : `str`
            The file to search through.
        detectorId : `int`
            The detector id to search for.
        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata: `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.
        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        log = lsst.log.Log.getLogger("VircamRawFormatter")
        log.debug("Did not find detector=%s at expected HDU=%s in %s: scanning through all HDUs.",
                  detectorId,
                  detectorId, detector_to_hdu[detectorId],
                  filename)

        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            metadata = fitsData.readMetadata()
            if metadata['ESO DET CHIP NO'] == detectorId:
                return i, metadata
        else:
            raise ValueError(f"Did not find detectorId={detectorId} as CCDNUM in any HDU of {filename}.")

    def _determineHDU(self, detectorId):
        """Determine the correct HDU number for a given detector id.
        Parameters
        ----------
        detectorId : `int`
            The detector id to search for.
        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata : `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.
        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        filename = self.fileDescriptor.location.path
        try:
            index = detector_to_hdu[detectorId]
            #print('detectorId {} type'.format(detectorId),type(detectorId))
            metadata = lsst.afw.fits.readMetadata(filename, index)
            if metadata['ESO DET CHIP NO'] != detectorId:
                # the detector->HDU mapping is different in this file: try scanning
                return self._scanHdus(filename, detectorId)
            else:
                fitsData = lsst.afw.fits.Fits(filename, 'r')
                fitsData.setHdu(index)
                return index, metadata
        except lsst.afw.fits.FitsError:
            # if the file doesn't contain all the HDUs of "normal" files, try scanning
            return self._scanHdus(filename, detectorId)

#     def readMetadata(self):
#         #Currently hacking to merge in required primary keys
#         filename = self.fileDescriptor.location.path
#         index, metadata = self._determineHDU(self.dataId['detector'])
#         #print("1",metadata)
#         primaryMetadata=lsst.afw.fits.readMetadata(filename, 0)
#         for k in ["ESO TEL POSANG","ESO INS THERMAL AMB MEAN","ESO TEL ALT","ESO TEL AZ"]:
#             metadata.setFloat(
#                 k,
#                 primaryMetadata.get(k))
#         astro_metadata_translator.fix_header(metadata,translator_class=VircamTranslator)
#         #VircamTranslator.fix_header(metadata, self.dataId['instrument'], self.dataId['exposure'])#
#         #print("2",metadata)
#         
#         return metadata
        
#Code above replaced by below from obs_lsst to use latest api
    def readMetadata(self):
        """Read all header metadata directly into a PropertyList.
        Specialist version since some of our data does not
        set INHERIT=T so we have to merge the headers manually.
        Returns
        -------
        metadata : `~lsst.daf.base.PropertyList`
            Header metadata.
        """
        file = self.fileDescriptor.location.path
        phdu = lsst.afw.fits.readMetadata(file, 0)
        index, md = self._determineHDU(self.dataId['detector'])
        if "INHERIT" in phdu:
            # Trust the inheritance flag
            return super().readMetadata()

        # Merge ourselves
        md = merge_headers([phdu, md],
                           mode="overwrite")
        #fix_header(md)
        astro_metadata_translator.fix_header(md,translator_class=VircamTranslator)
        #print('md:',md)
        return md
        
        
        
    def _createSkyWcsFromMetadata(self):
        # We need to know which direction the chip is "flipped" in order to
        # make a sensible WCS from the header metadata.
        wcs = makeSkyWcs(self.metadata, strip=True)
        dimensions = bboxFromMetadata(self.metadata).getDimensions()
        center = Point2D(dimensions/2.0)
        return wcs #makeFlippedWcs(wcs, self.FLIP_LR, self.FLIP_TB, center)

#     def readImage(self):
#         if self.fileDescriptor.parameters:
#             # It looks like the Gen2 std_raw code wouldn't have handled
#             # flipping vs. subimages correctly, so we won't bother to either.
#             # But we'll make sure no one tries to get a subimage, rather than
#             # doing something confusing.
#             raise NotImplementedError("Formatter does not support subimages.")
#         image = lsst.afw.image.ImageF(self.fileDescriptor.location.path, index)
#         return flipImage(image, self.FLIP_LR, self.FLIP_TB)

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        image = lsst.afw.image.ImageF(self.fileDescriptor.location.path, index)
        return flipImage(image, self.FLIP_LR, self.FLIP_TB)

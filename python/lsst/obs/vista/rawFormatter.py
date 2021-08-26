
"""Gen3 Butler Formatters for Vista raw data.
"""


import lsst.afw.fits
import lsst.afw.image
import lsst.log
from lsst.obs.base import FitsRawFormatterBase
from lsst.obs.base.utils import InitialSkyWcsError

import astro_metadata_translator

import logging
log = logging.getLogger("fitsRawFormatter")

from ._instrument import VIRCAM
from .vircamFilters import VIRCAM_FILTER_DEFINITIONS
from .translators import VircamTranslator


__all__ = ("VircamRawFormatter")


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
        useMetadataWcs=True
        if not self.isOnSky():
            # This is not an on-sky observation
            return None

        skyWcs = self._createSkyWcsFromMetadata()

        if useMetadataWcs:
            msg = "VIRCAM camera geom not set. Defaulting to metadata-based SkyWcs."
            log.warning(msg)
            if skyWcs is None:
                raise InitialSkyWcsError("Failed to create both metadata and boresight-based SkyWcs."
                                         "See warnings in log messages for details.")
            return skyWcs

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
            print('detectorId {} type'.format(detectorId),type(detectorId))
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

    def readMetadata(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        #print(metadata)
        astro_metadata_translator.fix_header(metadata,translator_class=VircamTranslator)
        #VircamTranslator.fix_header(metadata, self.dataId['instrument'], self.dataId['exposure'])#
        #print(metadata)
        return metadata

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        return lsst.afw.image.ImageF(self.fileDescriptor.location.path, index)

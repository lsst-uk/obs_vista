
"""Gen3 Butler Formatters for Vista raw data.
"""



import lsst.afw.fits
import lsst.afw.image
import lsst.log
from lsst.obs.base import FitsRawFormatterBase

from ._instrument import VISTA
from .vistaFilters import VISTA_FILTER_DEFINITIONS
from .translators import VistaTranslator

__all__ = ("VistaRawFormatter")


# The mapping of detector id to HDU in raw files for "most" DECam data.
# We try this first before scaning the HDUs manually.
detector_to_hdu = {
    0:1,
    1:2,
    2:3,
    3:4,
    4:5,
    5:6,
    6:7,
    7:8,
    8:9,
    9:10,
    10:11,
    11:12,
    12:13,
    13:14,
    14:15,
    15:16}


class VistaRawFormatter(FitsRawFormatterBase):
    translatorClass = VistaTranslator
    filterDefinitions = VISTA_FILTER_DEFINITIONS

    def getDetector(self, id):
        return VISTA().getCamera()[id]

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
        log = lsst.log.Log.getLogger("VistaRawFormatter")
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
            metadata = lsst.afw.image.readMetadata(filename, index)
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
        VistaTranslator.fix_header(metadata)
        return metadata

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId['detector'])
        return lsst.afw.image.ImageI(self.fileDescriptor.location.path, index)



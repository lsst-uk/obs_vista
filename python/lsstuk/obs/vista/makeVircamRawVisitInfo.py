from lsst.geom import degrees  
from lsst.afw.coord import Observatory
from lsst.obs.base import MakeRawVisitInfoViaObsInfo

from .translators import VircamTranslator

__all__ = ["MakeVircamRawVisitInfo"]


class MakeVircamRawVisitInfo(MakeRawVisitInfoViaObsInfo):
    """Make a VisitInfo from the FITS header of a VISTA image
    """
    metadataTranslator = VircamTranslator


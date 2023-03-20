# from lsst.afw.geom import degrees  # Failed in 20.0.0
from lsst.geom import degrees  # Many basic astro classes moved from afw.geom to geom
from lsst.afw.coord import Observatory
from lsst.obs.base import MakeRawVisitInfoViaObsInfo
from .translators import VircamTranslator

__all__ = ["MakeVircamRawVisitInfo"]


class MakeVircamRawVisitInfo(MakeRawVisitInfoViaObsInfo):
    """Make a VisitInfo from the FITS header of a VISTA image
    """
    metadataTranslator = VircamTranslator


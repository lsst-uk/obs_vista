"""Butler instrument description for VISTA.
"""

#__all__ = ("VISTA")

import os

from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument, yamlCamera
from lsst.obs.base.gen2to3 import TranslatorFactory, PhysicalFilterToBandKeyHandler
#from lsst.obs.base.gen2to3.translators import  AbstractToPhysicalFilterKeyHandler
from lsst.obs.vista.vistaFilters import VISTA_FILTER_DEFINITIONS

from lsst.daf.butler.core.utils import getFullTypeName
from lsst.utils import getPackageDir
from .translators import VistaTranslator

class VISTA(Instrument):
    filterDefinitions = VISTA_FILTER_DEFINITIONS
    policyName = "vista"
    #obsDataPackage = "obs_vista_data"  # What is this?

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        packageDir = getPackageDir("obs_vista")
        self.configPaths = [os.path.join(packageDir, "config")]

    @classmethod
    def getName(cls):
        return "VIRCAM"

    def getCamera(self):
        #path = os.path.join(getPackageDir("obs_vista"), self.policyName, "camGeom")
        #config = CameraConfig()
        #config.load(os.path.join(path, "camera.py"))
        #return makeCameraFromPath(
        #    cameraConfig=config,
        #    ampInfoPath=path,
        #    shortNameFunc=lambda name: name.replace(" ", "_"),
        #)
        #Gen 3 yaml camera
        path = os.path.join(
            getPackageDir("obs_vista"), 
            "camera", 
            'vista.yaml')
        return yamlCamera.makeCamera(path)

    def register(self, registry):
        camera = self.getCamera()
        obsMax = 2**31  #What is this? VISTA visit numbers will not go above this I think
        with registry.transaction():
            registry.syncDimensionData(
                "instrument",
                {
                   "name": self.getName(), 
                   "detector_max": 16, 
                   "visit_max": obsMax, 
                   "exposure_max": obsMax,
                   "class_name": getFullTypeName(self),
                 }
            ) 

            for detector in camera:
                registry.syncDimensionData(
                    "detector",
                    {
                        "instrument": self.getName(),
                        "id": detector.getId(),
                        "full_name": detector.getName(),
                        "name_in_raft": detector.getName()[1:],
                        "raft": detector.getName()[0],
                        "purpose": str(detector.getType()).split(".")[-1],
                    }
                )

            self._registerFilters(registry)

    def getRawFormatter(self, dataId):
        # local import to prevent circular dependency
        from .rawFormatter import VistaRawFormatter
        return VistaRawFormatter
    #def makeDataIdTranslatorFactory(self):
        '''
        Needed to register instrument
        '''
        #pass

    def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
    #    # Docstring inherited from lsst.obs.base.Instrument.
        factory = TranslatorFactory()
        factory.addGenericInstrumentRules(
            self.getName(), 
            calibFilterType="abstract_filter",
            detectorKey="ccdnum"
        )
        # VISTA calibRegistry entries are abstract_filters, but we need physical_filter
        # in the gen3 registry. 
        #UPDATE seems to have been superseeded by band
        #factory.addRule(AbstractToPhysicalFilterKeyHandler(self.filterDefinitions),
                        #instrument=self.getName(),
                        #gen2keys=("filter",),
                        #consume=("filter",),
                        #datasetTypeName="cpFlat")
        # Translate Gen2 `filter` to band if it hasn't been consumed
        # yet and gen2keys includes tract.
        factory.addRule(PhysicalFilterToBandKeyHandler(self.filterDefinitions),
                        instrument=self.getName(), gen2keys=("filter", "tract"), consume=("filter",))
        return factory
    #def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
        # Docstring inherited from lsst.obs.base.Instrument.
        #factory = TranslatorFactory()
        #factory.addGenericInstrumentRules(self.getName(), calibFilterType="band",detectorKey="ccdnum")
        # Translate Gen2 `filter` to band if it hasn't been consumed
        # yet and gen2keys includes tract.
        #factory.addRule(PhysicalFilterToBandKeyHandler(self.filterDefinitions),
                        #instrument=self.getName(), gen2keys=("filter", "tract"), consume=("filter",))
        #return factory
"""
    def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
        # Docstring inherited from lsst.obs.base.Instrument.
        factory = TranslatorFactory()
        factory.addGenericInstrumentRules(self.getName(), calibFilterType="band",
                                          detectorKey="ccdnum")
        # DECam calibRegistry entries are bands or aliases, but we need
        # physical_filter in the gen3 registry.
        factory.addRule(_DecamBandToPhysicalFilterKeyHandler(self.filterDefinitions),
                        instrument=self.getName(),
                        gen2keys=("filter",),
                        consume=("filter",))
        return factory

class _DecamBandToPhysicalFilterKeyHandler(PhysicalFilterToBandKeyHandler):
    A specialization of `~lsst.obs.base.gen2to3.BandToPhysicalKeyHandler`
    that allows filter aliases to be used as alternative band names.
    Parameters
    ----------
    filterDefinitions : `lsst.obs.base.FilterDefinitionCollection`
        The filters to translate from Gen 2 to Gen 3.
    

    __slots__ = ("_aliasMap",)

    def __init__(self, filterDefinitions):
        super().__init__(filterDefinitions)
        self._aliasMap = {alias: d.physical_filter for d in filterDefinitions for alias in d.alias}

    def extract(self, gen2id, *args, **kwargs):
        # Expect _aliasMap to be small, so try it first
        gen2Filter = gen2id["filter"]
        if gen2Filter in self._aliasMap:
            return self._aliasMap[gen2Filter]
        else:
            return super().extract(gen2id, *args, **kwargs) 
"""

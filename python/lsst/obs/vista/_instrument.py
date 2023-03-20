"""Butler gen3 instrument description for VISTA.

We use VIRCAM as instrument name.
"""


__all__ = ("VIRCAM",)


import os

from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument, yamlCamera
#from lsst.obs.base.gen2to3 import TranslatorFactory, PhysicalFilterToBandKeyHandler, BandToPhysicalFilterKeyHandler

from lsst.obs.vista.vircamFilters import VIRCAM_FILTER_DEFINITIONS
#from lsst.daf.butler.core.utils import getFullTypeName
from lsst.utils.introspection import get_full_type_name
from lsst.utils import getPackageDir
# Comment-out the following line if you put .translators/necam.py in the
# astro_metadata_translator repository:
from .translators import VircamTranslator


class VIRCAM(Instrument):
    filterDefinitions = VIRCAM_FILTER_DEFINITIONS
    #policyName = "vircam"

    # obsDataPackage = "obs_vista_data"  # What is this?

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
        # return makeCameraFromPath(
        #    cameraConfig=config,
        #    ampInfoPath=path,
        #    shortNameFunc=lambda name: name.replace(" ", "_"),
        # )
        # Gen 3 yaml camera
        path = os.path.join(
            getPackageDir("obs_vista"),
            "camera",
            'vircam.yaml')
        return yamlCamera.makeCamera(path)

#     def register(self, registry):
#         camera = self.getCamera()
#         obsMax = 2**31  # What is this? VISTA visit numbers will not go above this I think
#         with registry.transaction():
#             registry.syncDimensionData(
#                 "instrument",
#                 {
#                     "name": self.getName(),
#                     "detector_max": 16,
#                     "visit_max": obsMax,
#                     "exposure_max": obsMax,
#                     "class_name": getFullTypeName(self),
#                 }
#             )
# 
#             for detector in camera:
#                 registry.syncDimensionData(
#                     "detector",
#                     {
#                         "instrument": self.getName(),
#                         "id": detector.getId(),
#                         "full_name": detector.getName(),
#                         "name_in_raft": detector.getName()[1:],
#                         "raft": detector.getName()[0],
#                         "purpose": str(detector.getType()).split(".")[-1],
#                     }
#                 )
# 
#             self._registerFilters(registry)
    def register(self, registry, update=False):
        # Docstring inherited from Instrument.register
        camera = self.getCamera()
        # The maximum values below make Gen3's ObservationDataIdPacker produce
        # outputs that match Gen2's ccdExposureId.
        obsMax = 2**31
        with registry.transaction():
            registry.syncDimensionData(
                "instrument",
                {
                    "name": self.getName(),
                    "detector_max": 16,
                    "visit_max": obsMax,
                    "exposure_max": obsMax,
                    #"class_name": getFullTypeName(self),
                    "class_name": get_full_type_name(self),
                },
                update=update
            )
            for detector in camera:
                registry.syncDimensionData(
                    "detector",
                    {
                        "instrument": self.getName(),
                        "id": detector.getId(),
                        "full_name": detector.getName(),
                        # TODO: make sure these definitions are consistent with
                        # those extracted by astro_metadata_translator, and
                        # test that they remain consistent somehow.
                        "name_in_raft": detector.getName()[1:], #detector.getName().split("_")[1],
                        "raft": detector.getName().split("_")[0],
                        "purpose": str(detector.getType()).split(".")[-1],
                    },
                    update=update
                )
            self._registerFilters(registry, update=update)

    def getRawFormatter(self, dataId):
        # local import to prevent circular dependency

        from .rawFormatter import VircamRawFormatter
        return VircamRawFormatter

#     def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
#        # Docstring inherited from lsst.obs.base.Instrument.
#        factory = TranslatorFactory()
#        factory.addGenericInstrumentRules(
#            self.getName(),
#            calibFilterType="abstract_filter",
#            detectorKey="ccdnum"
#        )
#         # VISTA calibRegistry entries are abstract_filters, but we need physical_filter
#         # in the gen3 registry.
#         # UPDATE seems to have been superseeded by band
# #         factory.addRule(AbstractToPhysicalFilterKeyHandler(self.filterDefinitions),
# #                        instrument=self.getName(),
# #                        gen2keys=("filter",),
# #                        consume=("filter",),
# #                        datasetTypeName="cpFlat")
#        # Translate Gen2 `filter` to band if it hasn't been consumed
#        # yet and gen2keys includes tract.
#        factory.addRule(PhysicalFilterToBandKeyHandler(self.filterDefinitions),
#                        instrument=self.getName(), gen2keys=("filter", "tract"), consume=("filter",))
#        return factory
#     def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
#         # Docstring inherited from lsst.obs.base.Instrument.
#         factory = TranslatorFactory()
#         factory.addGenericInstrumentRules(self.getName())
#         # Translate Gen2 `filter` to band if it hasn't been consumed
#         # yet and gen2keys includes tract.
#         factory.addRule(PhysicalFilterToBandKeyHandler(self.filterDefinitions),
#                         instrument=self.getName(), gen2keys=("filter", "tract"), consume=("filter",))
#         return factory
#     def makeDataIdTranslatorFactory(self) -> TranslatorFactory:
#         # Docstring inherited from lsst.obs.base.Instrument.
#         factory = TranslatorFactory()
#         factory.addGenericInstrumentRules(self.getName(), calibFilterType="band",
#                                           detectorKey="ccdnum")
#         # DECam calibRegistry entries are bands, but we need physical_filter
#         # in the gen3 registry.
#         factory.addRule(BandToPhysicalFilterKeyHandler(self.filterDefinitions),
#                         instrument=self.getName(),
#                         gen2keys=("filter",),
#                         consume=("filter",),
#                         datasetTypeName="cpFlat")
#         return factory

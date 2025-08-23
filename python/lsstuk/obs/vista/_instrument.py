"""Butler gen3 instrument description for VISTA.

We use VIRCAM as instrument name.
"""


__all__ = ("VIRCAM",)


import os

from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument, yamlCamera
from lsst.utils.introspection import get_full_type_name
from lsst.utils import getPackageDir

#Local imports
from .translators import VircamTranslator
from .vircamFilters import VIRCAM_FILTER_DEFINITIONS

class VIRCAM(Instrument):
    filterDefinitions = VIRCAM_FILTER_DEFINITIONS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        packageDir = getPackageDir("obs_vista")

        # Look for an environment variable to decide which config profile to use
        profile = os.environ.get("OBS_VISTA_PROFILE", None)
        if profile is None:
            raise RuntimeError("You must set OBS_VISTA_PROFILE to choose a config profile "
                "(e.g. HSC, comCam, lsstCam)."
            )

        # Normalize input (case-insensitive) and map to canonical directory names
        profile_map = {
            "hsc": "HSC",
            "comcam": "comCam",
            "lsstcam": "lsstCam",
        }


        profile_key = profile.lower()
        if profile_key not in profile_map:
            raise RuntimeError(
                f"Unknown OBS_VISTA_PROFILE='{profile}'. "
                f"Allowed values: {list(profile_map.keys())}"
            )

        configDir = os.path.join(packageDir, "config", profile_map[profile_key])

        if not os.path.isdir(configDir):
            raise RuntimeError(
                f"Requested obs_vista profile '{profile}' but no config directory found at {configDir}"
            )

        # Register the selected config directory
        self.configPaths = [configDir]


    @classmethod
    def getName(cls):
        return "VIRCAM"

    def getCamera(self):

        path = os.path.join(
            getPackageDir("obs_vista"),
            "camera",
            'vircam.yaml')
        return yamlCamera.makeCamera(path)


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
                    "detector_max": 17,
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

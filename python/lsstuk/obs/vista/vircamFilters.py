from lsst.obs.base import FilterDefinition, FilterDefinitionCollection


VIRCAM_FILTER_DEFINITIONS = FilterDefinitionCollection(

    FilterDefinition(
        band="Clear",
        physical_filter="NONE",
        alias={
            "Clear", "NONE", "None",
            "Unrecognised", "UNRECOGNISED",
            "Unrecognized", "UNRECOGNIZED",
            "NOTSET",
        },
    ),

    # VIRCAM
    FilterDefinition(
        physical_filter="VIRCAM-Z",
        band="Z",
    ),
    FilterDefinition(
        physical_filter="VIRCAM-Y",
        band="Y",
    ),
    FilterDefinition(
        physical_filter="VIRCAM-J",
        band="J",
    ),
    FilterDefinition(
        physical_filter="VIRCAM-H",
        band="H",
    ),
    FilterDefinition(
        physical_filter="VIRCAM-Ks",
        band="K",
    ),

    # External optical bands used in joint HSC/ComCam/LSSTCam + VIRCAM processing.
    FilterDefinition(
        physical_filter="EXT-U",
        band="u",
        alias={"ComCam-u", "u_24"},
    ),
    FilterDefinition(
        physical_filter="EXT-G",
        band="g",
        alias={"W-S-G+", "ComCam-g", "g_6"},
    ),
    FilterDefinition(
        physical_filter="EXT-R",
        band="r",
        alias={"W-S-R+", "ComCam-r", "r_57"},
    ),
    FilterDefinition(
        physical_filter="EXT-I",
        band="i",
        alias={"W-S-I+", "ComCam-i", "i_39"},
    ),
    FilterDefinition(
        physical_filter="EXT-Z",
        band="z",
        alias={"W-S-Z+", "ComCam-z", "z_20"},
    ),
    FilterDefinition(
        physical_filter="EXT-Y",
        band="y",
        alias={"W-S-ZR", "ComCam-y", "y_10"},
    ),
)

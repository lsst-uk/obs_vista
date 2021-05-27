#!/usr/bin/env python


import lsst.pipe.base as pipeBase
import lsst.pex.config as pexConfig

__all__ = ["VistaNullIsrConfig", "VistaNullIsrTask"]


class VistaNullIsrConfig(pexConfig.Config):
    doWrite = pexConfig.Field(
        dtype=bool,
        doc="Persist loaded data as a postISRCCD? The default is false, to avoid duplicating data.",
        default=False,
    )
    datasetType = pexConfig.Field(
        dtype=str,
        doc="Dataset type for input data; read by ProcessCcdTask; users will typically leave this alone",
        default="raw",
    )


class VistaNullIsrTask(pipeBase.Task):
    """Load an "raw" exposure as a post-ISR CCD exposure.

    Load "instcal" exposures from the community pipeline as a post-ISR exposure,
    and optionally persist it as a `postISRCCD`.

    This is used to retarget the `isr` subtask in `ProcessCcdTask` when you prefer to use
    the community pipeline instead of the LSST software stack to perform ISR on DECam images.
    """
    ConfigClass = VistaNullIsrConfig
    _DefaultName = "isr"

    @pipeBase.timeMethod
    def runDataRef(self, sensorRef):
        """Load a VISTA community pipeline "instcal" exposure as a post-ISR CCD exposure

        Parameters
        ----------
        sensorRef : `lsst.daf.persistence.butlerSubset.ButlerDataRef`
            Butler data reference for post-ISR exposure.

        Returns
        -------
        result : `struct`
            A pipeBase.Struct with fields:

            - ``exposure`` : Exposure after application of ISR: the "instcal" exposure, unchanged.

        """
        self.log.info("Loading VISTA community pipeline file %s" % (sensorRef.dataId))
     
        
        exposure = sensorRef.get("raw", immediate=True)
        if self.config.doWrite:
            sensorRef.put(exposure, "postISRCCD")

        return pipeBase.Struct(
            exposure=exposure,
        )

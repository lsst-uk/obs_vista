#!/usr/bin/env python
#

from lsst.ip.isr.isrTask import IsrTask, IsrTaskConfig


__all__ = ["VistaIsrConfig", "VistaIsrTask"]


class VistaIsrConfig(IsrTaskConfig):
    doApplyConfMap = pexConfig.Field(
        dtype=bool,
        doc="Apply the CASU VISTA confidence map to the exposure variance image if available.",
        default=False,
    )


class VistaIsrTask(IsrTask):
    """Load a CASU confidence map and apply it to the variance plane

    This is used to retarget the `isr` subtask in `ProcessCcdTask` when you prefer to use
    the community pipeline instead of the LSST software stack to perform ISR on DECam images.
    """
    ConfigClass = VistaIsrConfig
    _DefaultName = "isr"

    def applyConfidenceMapToAmpExposure(self, ampExposure, confMap=None):

        if confMap not None:
            maskedImage = ampExposure.getMaskedImage()
            maskedImage *= (100./confMap)

    @pipeBase.timeMethod
    def updateVariance(self, ampExposure, amp, overscanImage=None, ptcDataset=None):
        """Find the confidence map and modify the ampExposure sent to the variance method

        """
        #self.log.info("Loading VISTA community pipeline file %s" % (sensorRef.dataId))
        if self.config.doApplyConfMap:
            super().updateVariance(self, ampExposure, amp, overscanImage=None, ptcDataset=None)
            try:
                # get the confidence map using the dataRef for the exposure
                confMap = dataRef.get("confMap", immediate=True)
            except NoResults:
                confMap = None
            applyConfidenceMapToAmpExposure(self, ampExposure, confMap=confMap)
        else:
            super().updateVariance(self, ampExposure, amp, overscanImage=None, ptcDataset=None)

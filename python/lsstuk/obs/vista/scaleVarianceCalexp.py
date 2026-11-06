import lsst.pipe.base as pipeBase
import lsst.pipe.base.connectionTypes as connectionTypes

from lsst.meas.algorithms import ScaleVarianceTask
from lsst.pex.config import ConfigurableField


class ScaleVarianceCalexpConnections(
    pipeBase.PipelineTaskConnections,
    dimensions=("instrument", "visit", "detector"),
):
    inputExposure = connectionTypes.Input(
        doc="Calibrated exposure before variance normalization.",
        name="calexp_unscaled",
        storageClass="ExposureF",
        dimensions=("instrument", "visit", "detector"),
    )

    outputExposure = connectionTypes.Output(
        doc="Calibrated exposure after variance normalization.",
        name="calexp",
        storageClass="ExposureF",
        dimensions=("instrument", "visit", "detector"),
    )


class ScaleVarianceCalexpConfig(
    pipeBase.PipelineTaskConfig,
    pipelineConnections=ScaleVarianceCalexpConnections,
):
    scaleVariance = ConfigurableField(
        target=ScaleVarianceTask,
        doc="Empirically normalize the variance plane.",
    )


class ScaleVarianceCalexpTask(pipeBase.PipelineTask):
    ConfigClass = ScaleVarianceCalexpConfig
    _DefaultName = "scaleVarianceCalexp"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.makeSubtask("scaleVariance")

    def run(self, inputExposure):
        outputExposure = inputExposure.clone()

        factor = self.scaleVariance.run(
            outputExposure.getMaskedImage()
        )

        outputExposure.getMetadata().set(
            "VARIANCE_SCALE",
            factor,
        )

        self.log.info(
            "Applied calexp variance scale factor: %.8f",
            factor,
        )

        return pipeBase.Struct(
            outputExposure=outputExposure,
        )

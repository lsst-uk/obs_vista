#imports required by task definition - this cell should contain all the Python for the task 
#such that it can be directly copied to obs_vista/python/lsst/obs/vista/vircamIsrTask.py
from lsst.ip.isr.isrTask import IsrTask, IsrTaskConfig, IsrTaskConnections
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.pipe.base.connectionTypes as cT
from lsst.utils.timer import timeMethod
import lsst.geom as geom
import numpy as np

__all__ = ["VircamIsrConfig", "VircamIsrTask", "VircamIsrTaskConnections"]


class VircamIsrTaskConnections(IsrTaskConnections):
    confidence = cT.PrerequisiteInput(
        name="confidence",
        doc="Confidence map associated with input exposure to process.",
        storageClass="ExposureF",
        dimensions=["instrument", "exposure", "detector"],
    )
    def __init__(self, *, config=None):
        super().__init__(config=config)

        if config.doVircamConfidence is not True:
            self.prerequisiteInputs.discard("confidence")

class VircamIsrConfig(IsrTaskConfig,
        #pipelineConnections=IsrTaskConnections):
        pipelineConnections=VircamIsrTaskConnections):
    doVircamConfidence = pexConfig.Field(
        dtype=bool,
        doc="Apply the CASU VISTA confidence map to the exposure variance image if available.",
        default=False,
    )
    
    updateVircamBBox = pexConfig.Field(
        dtype=bool,
        doc="Correct the BBox of the exposure to account for dithering for stack.",
        default=False,
    )
    
    def setDefaults(self):
        IsrTask.ConfigClass.setDefaults(self)

class VircamIsrTask(IsrTask):
    """Load a CASU confidence map and apply it to the variance plane

    This is used to retarget the `isr` subtask in `ProcessCcdTask` when you prefer to use
    the community pipeline instead of the LSST software stack to perform ISR on DECam images.
    """
    ConfigClass = VircamIsrConfig
    _DefaultName = "isr"
 
    @timeMethod
    def run(self, ccdExposure, *, camera=None, bias=None, linearizer=None,
            crosstalk=None, crosstalkSources=None,
            dark=None, flat=None, ptc=None, bfKernel=None, bfGains=None, defects=None,
            fringes=pipeBase.Struct(fringes=None), opticsTransmission=None, filterTransmission=None,
            sensorTransmission=None, atmosphereTransmission=None,
            detectorNum=None, strayLightData=None, illumMaskedImage=None,
            isGen3=False,
            confidence=None #additional argument passed to overwritten method
            ):
        """Execute the parent run method and apply confidence and gain if requested"""
        self.log.info("VISTA: Running vircamIsrTask." )

        
        if self.config.updateVircamBBox:
            self.vircamUpdateDetector(ccdExposure)
        
        output= super().run(ccdExposure, camera=camera, bias=bias, linearizer=linearizer,
            crosstalk=crosstalk, crosstalkSources=crosstalkSources,
            dark=dark, flat=flat, ptc=ptc, bfKernel=bfKernel, bfGains=bfGains, defects=defects,
            fringes=fringes, opticsTransmission=opticsTransmission, filterTransmission=filterTransmission,
            sensorTransmission=sensorTransmission, atmosphereTransmission=atmosphereTransmission,
            detectorNum=detectorNum, strayLightData=strayLightData, illumMaskedImage=illumMaskedImage,
            #isGen3=isGen3,
            #additional argument not passed to parent method
            )
        
      
        #Make the VISTA specific variance plane
        if self.config.doVircamConfidence and confidence is not None:
            self.vircamUpdateVariance(output.exposure,confidence=confidence)
        if self.config.doVircamConfidence and confidence is None:
            self.log.info("VISTA: doVircamConfidence is True but no confidence map is available." )

        # output.outputExposure=output.exposure
        return output

    def vircamUpdateVariance(self, exposure, *, confidence=None):
        """Make a VIRCAM CASU based variance plane from the confidence map

        Parameters
        ----------
        exposure : `lsst.afw.image.Exposure`
            The exposure after running parent ISR methods.  The
            exposure is modified by this method.

        confidence : `lsst.afw.image.Exposure`
            The CASU confidence map
        """
       
        expNum=exposure.getInfo().getMetadata().getAsInt('NICOMB')
        sky=exposure.getInfo().getMetadata().getAsDouble('SKYLEVEL')
        amp=exposure.getDetector().getAmplifiers()[0]
        gain=amp.getGain()
        readNoise=amp.getReadNoise()
            
        var = exposure.getVariance()
        img = exposure.getImage()
        #cut the cropped region out of the confidence map
        conf=confidence.image.array[:var.array.shape[0],:var.array.shape[1]]
        #flip the confidence map to account for image flipping
        #NOTE: Flipping must be consistent with camera.yaml and rawFormatter
        conf=np.flipud(np.fliplr(conf))
        effNum=expNum*conf/100 #effective exposure number
        #Apply CASU variance from confidence, image, sky in stages to optimise memory use
        var.array=(1+effNum)/effNum
        var.array*=readNoise**2
        var.array+=img.array/gain
        var.array+=sky/(effNum*gain)
        var.array/=effNum

        self.log.info("VISTA: Effective exposure number reset using CASU confidence map." )
        
        #Now lets modify the mask using the low confidence pixels
        mask=exposure.getMask()
        #Mask all pixels with confidence below 20 as bad
        mask.array[conf<20]|=mask.getPlaneBitMask('BAD')
        self.log.info("VISTA: Pixels with confidence <20% flagged BAD.")



    def vircamUpdateDetector(self, ccdExposure):
        """Update the detector bounding boxes to match the image

        VIRCAM CASU stacks are different sizes depending on 
 
        Parameters
        ----------
        ccdExposure : `lsst.afw.image.Exposure`
            The exposure to modify the bounding boxes for.

        """
        detector=ccdExposure.getDetector()
        #update BBox to image size
        BBox = geom.Box2I(geom.Point2I(0, 0), geom.Extent2I(
            ccdExposure.getImage().array.shape[1],
            ccdExposure.getImage().array.shape[0]
        ))
        self.log.info("VISTA: Updating detector BBox to contain full stacked image [{},{}].".format(
            ccdExposure.getImage().array.shape[1],
            ccdExposure.getImage().array.shape[0]) )
        detBuilder=detector.rebuild()
        detBuilder.setBBox(BBox)
        amplifier=detBuilder.getAmplifiers()[0]
        #ampBuilder=amplifier.rebuild()
        amplifier.setRawBBox(BBox)
        amplifier.setBBox(BBox)
        amplifier.setRawDataBBox(BBox)
        ccdExposure.setDetector(detBuilder.finish())

        
        


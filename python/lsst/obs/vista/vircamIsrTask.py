#!/usr/bin/env python
#

#imports required by task definition - this cell should contain all the Python for the task 
#such that it can be directly copied to obs_vista/python/lsst/obs/vista/vircamIsrTask.py
from lsst.ip.isr.isrTask import IsrTask, IsrTaskConfig, IsrTaskConnections
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.pipe.base.connectionTypes as cT
from lsst.utils.timer import timeMethod

__all__ = ["VircamIsrConfig", "VircamIsrTask", "VircamIsrTaskConnections"]


class VircamIsrTaskConnections(IsrTaskConnections):
    confidence = cT.PrerequisiteInput(
        name="confidence",
        doc="Confidence map associated with input exposure to process.",
        storageClass="Exposure",
        dimensions=["instrument", "exposure", "detector"],
    )
    def __init__(self, *, config=None):
        super().__init__(config=config)

        if config.doConfidence is not True:
            self.prerequisiteInputs.discard("confidence")

class VircamIsrConfig(IsrTaskConfig,
        #pipelineConnections=IsrTaskConnections):
        pipelineConnections=VircamIsrTaskConnections):
    doVircamConfidence = pexConfig.Field(
        dtype=bool,
        doc="Apply the CASU VISTA confidence map to the exposure variance image if available.",
        default=False,
    )
    
    updateVircamGain = pexConfig.Field(
        dtype=bool,
        doc="Correct the gain using the VIRCAM CASU stack exposure number. If doConfidence is True this change will be overwriten.",
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
        print(ccdExposure.getVariance().array.shape)
        print(ccdExposure.getImage().array[-1,-1])
        
        self.vircamUpdateDetector(ccdExposure)
        
        output= super().run(ccdExposure, camera=camera, bias=bias, linearizer=linearizer,
            crosstalk=crosstalk, crosstalkSources=crosstalkSources,
            dark=dark, flat=flat, ptc=ptc, bfKernel=bfKernel, bfGains=bfGains, defects=defects,
            fringes=fringes, opticsTransmission=opticsTransmission, filterTransmission=filterTransmission,
            sensorTransmission=sensorTransmission, atmosphereTransmission=atmosphereTransmission,
            detectorNum=detectorNum, strayLightData=strayLightData, illumMaskedImage=illumMaskedImage,
            isGen3=isGen3,
            #additional argument not passed to parent method
            )
        print(output.exposure.getVariance().array.shape)
        print(output.exposure.getImage().array[-1,-1])
        print(ccdExposure.getImage().array[-1,-1])
        
        print(output.exposure.getVariance().array[1000,1000])
        #Make the VISTA specific variance plane
        self.vircamUpdateVariance(output.exposure,confidence=confidence)
        print(output.exposure.getVariance().array[1000,1000])
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
       
        if self.config.updateVircamGain:
            self.log.info("VISTA: Variance plane reset using updated gain based on CASU stack exposure number." )
            #get exposure number and update gain
            expNum=exposure.getInfo().getMetadata().getAsInt('ESO DET NDIT')
            amp=exposure.getDetector().getAmplifiers()[0]
            gain=amp.getGain()
            readNoise=amp.getReadNoise()
            gain*=(expNum/6) #6 is default value set in camera. This is the only difference compared to updateVariance.
            self.log.info("VISTA: CASU stack built from {} exposures updating gain by factor {}.".format(expNum,gain) )
            var = exposure.getVariance()
            var[:] = exposure.getImage()
            var /= gain
            var += readNoise**2
            
        if self.config.doVircamConfidence and confidence is not None:
            self.log.info("VISTA: Variance plane reset using CASU confidence map." )
            #We are modifying the original variance set by lsst.ip.isr.isrFunctions.updateVariance
            var = exposure.getVariance()
            #cut the cropped region out of the confidence map
            conf=confidence.image.array[:var.array.shape[0],:var.array.shape[1]]
            #flip the confidence map to account for image flipping
            #NOTE: Flipping must be consistent with camera.yaml and rawFormatter
            conf=np.flipud(np.fliplr(conf))
            #Apply CASU variance from confidence and image
            var.array*=100/conf
            #Now lets modify the mask using the low confidence pixels
            mask=exposure.getMask()
            #Mask all pixels with confidence below 20 as bad
            mask.array[conf<20]|=mask.getPlaneBitMask('BAD')
   
        elif self.config.doVircamConfidence and confidence is None:
            self.log.info("VISTA: doConfidence is True but no confidence map is given." )
            
        if not self.config.updateVircamGain and not self.config.doVircamConfidence:
            self.log.info("VISTA: Variance plane not modifed by vircamIsrTask." )


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
            ccdExposure.getImage().array.shape[1],ccdExposure.getImage().array.shape[0]))
        detBuilder=detector.rebuild()
        detBuilder.setBBox(BBox)
        amplifier=detBuilder.getAmplifiers()[0]
        #ampBuilder=amplifier.rebuild()
        amplifier.setRawBBox(BBox)
        amplifier.setBBox(BBox)
        amplifier.setRawDataBBox(BBox)
        ccdExposure.setDetector(detBuilder.finish())

        



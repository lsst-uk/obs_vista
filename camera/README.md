# The Camera files

The files here describe the VISTA VIRCAM Camera. We need to specify the pixel dimensions, gain, saturation and readout noise.

In this directory we must have a fits file for each ccd. Together these describe the VISTA camera. The buildDetectors script is modified from obs_necam to make the fits file for each ccd. 

The fits files currently present are made from an obs_subaru example fits files for each CCD and modifying key values. 

Saturation values are taken from :

http://casu.ast.cam.ac.uk/surveys-projects/vista/technical/linearity-sequences

and gain values are taken from 

http://casu.ast.cam.ac.uk/surveys-projects/vista/technical/vista-gain

The median gain is 4.2. Since gain is electrons per count the effective gain value is different for exposures and stacks. Since stacks are produced from six exposures:


gain_{stack} = gain_{exposure}/6

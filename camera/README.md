# The Camera files

The files here describe the VISTA VIRCAM Camera. We need to specify the pixel dimensions, gain, saturation and readout noise.

In gen 2 we had a fits file for each detector. These have been replaced with a single yaml file and will be deleted when gen 2 functionality is deprecated.

The camera geometry must be specified in order to generate the first WCS solution before fitting which must at least generate a list of calibrators that overlap with the exposures.

Saturation values are taken from :

http://casu.ast.cam.ac.uk/surveys-projects/vista/technical/linearity-sequences

and gain values are taken from 

http://casu.ast.cam.ac.uk/surveys-projects/vista/technical/vista-gain

The median gain is 4.2 [e-/ADU]. The LSST Science Pipelines use an alternative definition of gain to CASU so all CASU gains are inverted to give units in [ADU/e-].

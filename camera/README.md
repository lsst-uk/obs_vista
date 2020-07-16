# The Camera files

In this directory we must have a camera.py and a fits file for each ccd. Together these describe the VISTA camera. We need these to run the ingestImages.py command line task. I am modifying the buildDetectors script from obs_necam to make the fits file for each ccd. This was developed with gen2 and needs updating.

The fits files currently present are a hack based on opening an obs_subaru example fits files for each CCD and modifying key values. In due course we will develop the buildDetector.py code to produce these possibly based on some external descriptions of the CCDs.

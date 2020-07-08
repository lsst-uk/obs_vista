import os.path
from lsst.utils import getPackageDir

'''
ProcessCcd runs a lot of processes, but they are split into three broad sections:
- ISR (instrument signature removal);
- Image Characterisation (background subtraction, PSF modelling, CR repair);
- Imaga Calibration (astrometric and photometric calibration).

Subsequently, there are a **huge** number of config parameters that one can adjust for processCcd. To keep things a little tidier, I like to split the processCcd's config parameters into three other config files corresponding to each of the above three sections. 
'''

#Grab the path to this config directory:
configDir = os.path.join(getPackageDir("obs_necam"), "config")

#Load ISR configurations:
config.isr.load(os.path.join(configDir, "isr.py"))

#Characterise:
config.isr.load(os.path.join(configDir, "characterise.py"))

#Load Calibrate configurations
config.doCalibrate = False
config.calibrate.load(os.path.join(configDir, "calibrate.py"))
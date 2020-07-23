"""
VISTA specific overirdes for ProcessCcdTask
"""
import os.path
from lsst.utils import getPackageDir

'''
ProcessCcd runs a lot of processes, but they are split into three broad sections:
- ISR (instrument signature removal);
- Image Characterisation (background subtraction, PSF modelling, CR repair);
- Imaga Calibration (astrometric and photometric calibration).

Subsequently, there are a **huge** number of config parameters that one can adjust for processCcd. To keep things a little tidier, I like to split the processCcd's config parameters into three other config files corresponding to each of the above three sections. 


At this stage we are skipping these steps so we just want the code to directly give the premade stacks.
'''

#Grab the path to this config directory:
configDir = os.path.join(getPackageDir("obs_vista"), "config")

#Load ISR configurations:
config.isr.load(os.path.join(configDir, "isr.py"))

#Characterise:
config.isr.load(os.path.join(configDir, "characterise.py"))

#Load Calibrate configurations
config.doCalibrate = True
config.calibrate.load(os.path.join(configDir, "calibrate.py"))


# Following added to use panstarrs reference catalogue
# see https://community.lsst.org/t/pan-starrs-reference-catalog-in-lsst-format/1572
# We will need a different photometric reference catalogue for the JHKs bands - 2MASS?
#from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
#config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.calibrate.astromRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
#config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.calibrate.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
#config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

#Tried this from goto:
#from lsst.meas.extensions.astrometryNet import ANetAstrometryTask
#config.astrometry.retarget(ANetAstrometryTask)
#from lsst.meas.extensions.astrometryNet import LoadAstrometryNetObjectsTask
#config.astromRefObjLoader.retarget(LoadAstrometryNetObjectsTask)
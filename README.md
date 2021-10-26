# obs_vista
VISTA (VIRCAM) specific configuration and tasks for the LSST Data Management Stack. The VISTA infrared camera (VIRCAM) instrument on the ESO Visible and Infrared Survey Telescope
for Astronomy (VISTA) telescope has produced a number of wide and deep surveys in the southern sky which are well matched with Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) fields. This package describes the camera and data products, allowing the LSST stack to import and manipulate the data. It will allow both processing of VISTA imaging with the stack independently as well as the production of joint VISTA/Rubin imaging and catalogue products.

## Overview

This code is a modification of the obs\_necam "Any cam" template; https://github.com/jrmullaney/obs_necam

The documenttation for this is at https://lsstcamdocs.readthedocs.io/en/latest/intro.html This documentation was developed during production of the obs package for the GOTO telescope.

The package is currently configured to work with the second generation 'Butler'. Development of a version compatible with the third generation Butler is ongoing. Note that we use the telescope name VISTA to describe the VIRCAM camera for simplicity. 

Folders:

- [camera](camera) Files containing information that describe the properties of VISTA (dimensions, gain etc).
- [config](config) Configuration files that tell the various stack process that access your data how to behave. The final data products will also contain automatically generated config files in case the standard here have changed or were overridden during processing.
- [policy](policy) Files describing the file structure and type of input and output data (e.g., image, table etc).
- [python/lsst](python/lsst) This is where all the scripts go that manipulate VISTA data
- [ups](ups) A file telling the [eups](https://developer.lsst.io/stack/eups-tutorial.html) system what other packages need to be set up to use this obs_package.

## Installation

After [installing the LSST stack]https://pipelines.lsst.io/install/newinstall.html() the obs_vista package must go in the stack folder which contains all the obs packages:


```Shell
cd $STACKPATH/stack/current/$SYSTEMTYPE/   # example stack directory
mkdir obs_vista
cd obs_vista
git clone https://github.com/lsst-uk/obs_vista.git
mv obs_vista 20.0.0-1   #Stack version 20.0.0 used for development and obs version 1
```

This will now be a git submodule so any git commands run inside this directory will interact with the obs_vista git repo and not the lsstsw repo. You now need to declare the package to EUPS.

```Shell
eups declare -t current obs_vista 20.0.0-1   # run once
setup obs_vista                              # run in every shell
```

Running 

```Shell
eups list
```

Should show the 20.0.0-1 version of obs_vista as current and setup. Check the setup has worked by running

```Shell
processCcd.py
```

### Updating the science pipelines

The pipelines are currently under active development. Given the latest release has been installed you can update to the latest weekly using:

```Shell
eups distrib install -t w_latest lsst_distrib
setup lsst_distrib -t w_latest
```

### Generation 3 Butler

The Generation 3 Butler pipeline is under development. An example generation 3 run is available here:

https://github.com/lsst-uk/lsst-ir-fusion/blob/master/dmu4/dmu4_Example/test_patch_gen3.sh

To run this you will need access to the VIDEO test data. This will be made available shortly.

### Generation 2 Butler

We are currently trying to maintain generation 2 functionality so the first prototype runs remain accessible. This functionality should be deprecated around the start of 2022 following which we will delete all the generation 2 prototype data. You will also need to create a `_mapper' file in the Butler data directory:

```Shell
echo "lsst.obs.vista.VistaMapper" > ./data/_mapper
```

After which the gen2 command line tasks should accept that data folder as a Butler repo to interact with. The gen3 obs_vista is under development.

## The Camera

The package is designed to work with all VISTA data products. The calibration of the
VIRCAM instrument on the ESO VISTA telescope is described in [González-Fernández et al.](2018 https://ui.adsabs.harvard.edu/abs/2018MNRAS.474.5459G/abstract)

There is also further information on the VISTA technical specifications on the CASU website http://casu.ast.cam.ac.uk/surveys-projects/vista/technical

The script [camera/buildDetectors.py](camera/buildDetectors.py) is used to create the camera definition. In the new generation 3 package this is stored in a single yaml file: [camera/camera.yaml](camera/camera.yaml).



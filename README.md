# obs_vista
VISTA (VIRCAM) specific configuration and tasks for the LSST Data Management Stack. It describes the camera and data products, allowing the LSST stack to import and manipulate the data.

## Overview

This code is a modification of the obs\_necam "Any cam" template; https://github.com/jrmullaney/obs_necam

The documenttation for this is at https://lsstcamdocs.readthedocs.io/en/latest/intro.html This documentation was developed during production of the obs package for the GOTO telescope.

As a first pass we have simply replaced Necam with VISTA throughout. Note that we use standard Python capitalisation schemes paying no heed to the VISTA capitalisation. Note also that I am using the telescope name VISTA to describe the VIRCAM camera for simplicity. 

Folders:

- [camera](camera) Files containing information that describe the properties of VISTA (dimensions, gain etc).
- [config](config) Configuration files that tell the various stack process that access your data how to behave.
- [policy](policy) Files describing the file structure and type of input and output data (e.g., image, table etc).
- [python/lsst](python/lsst) This is where all the scripts go that manipulate VISTA data
- [ups](ups) A file telling the [eups](https://developer.lsst.io/stack/eups-tutorial.html) system what other packages need to be set up to use this obs_package.

## Installation

After [installing the LSST stack]https://pipelines.lsst.io/install/newinstall.html() the obs_vista package must go in the folder which contains all the obs packages:


```Shell
cd $STACKPATH/stack/current/DarwinX86/   # example stack directory
mkdir obs_vista
cd obs_vista
git clone https://github.com/raphaelshirley/obs_vista.git
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

You will also need to create a _mapper file in the Butler data directory:

```Shell
echo "lsst.obs.vista.VistaMapper" > ./data/_mapper
```

After which the gen2 command line tasks should accept that data folder as a Butler repo to interact with. The gen3 obs_vista is under development.

## The Camera

The package is designed to work with all VISTA data products. The calibration of the
VIRCAM instrument on the ESO VISTA telescope is described in González-Fernández et al. 2018 https://ui.adsabs.harvard.edu/abs/2018MNRAS.474.5459G/abstract

There is also further information on the VISTA technical specifications on the CASU website http://casu.ast.cam.ac.uk/surveys-projects/vista/technical

The key numbers specified in [camera/camera.py](camera/camera.py) are:

| parameter   | value | unit |
|-------------|-------|------|
| pixel scale |       |      |
| dimensions  |       |      |
| name        |       |      |

The script [camera/buildDetectors.py](camera/buildDetectors.py) will be used to make a fits file describing each of the 16 CCDs. This is currently not running due to conflicts with the latest version of the stack.



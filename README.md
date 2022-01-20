# obs_vista
VISTA (VIRCAM) specific configuration and tasks for the LSST Data Management Stack. The VISTA infrared camera (VIRCAM) instrument on the ESO Visible and Infrared Survey Telescope
for Astronomy (VISTA) has produced a number of wide and deep surveys in the southern sky which are well matched with Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) fields. This package describes the camera and data products, allowing the LSST Science Pipelines to import and manipulate the data. It will allow both processing of VISTA imaging with the pipelines independently as well as the production of joint VISTA/Rubin imaging and catalogue products.

## Overview

This code is a modification of the [obs\_necam "Any cam"](https://github.com/jrmullaney/obs_necam) template. It also draws heavily on [obs\_subaru](https://github.com/lsst/obs_subaru), [obs\_decam](https://github.com/lsst/obs_decam), and other obs packages under development.

The package is currently configured to work with both the second generation 'Butler' and the evolving third generation version. All generation 2 code will be deprecated in the coming year. Note that we use the telescope name VISTA to describe the telescope and VIRCAM to describe the camera. 

Folders:

- [camera](camera) Files containing information that describe the properties of VIRCAM (dimensions, gain etc).
- [config](config) Configuration files that tell the various pipeline tasks that access your data how to behave. The final data products will also contain automatically generated config files in case the standards here have changed or were overridden during processing.
- [policy](policy) Files describing the file structure and type of input and output data (e.g., image, table etc). This is for the previous generation 2 middleware and will be deprecated.
- [python/lsst](python/lsst) This is where all the VISTA specific code and instrument classes go.
- [ups](ups) A file telling the [eups](https://developer.lsst.io/stack/eups-tutorial.html) system what other packages need to be set up to use this obs_package.

## Installation

After [installing the LSST stack](https://pipelines.lsst.io/install/newinstall.html) the obs_vista package must go in the stack folder which contains all the obs packages:


```Shell
cd $RUBIN_EUPS_PATH  # Stack directory set during installation
cd DarwinX86 # Typical mac system directory
mkdir obs_vista
cd obs_vista
git clone https://github.com/lsst-uk/obs_vista.git
mv obs_vista 22.0.0-1   #Stack version 22.0.0 used for development and obs version 1
```

This will now be a git submodule so any git commands run inside this directory will interact with the obs_vista git repo and not the lsstsw repo. You now need to declare the package to EUPS.

```Shell
eups declare -t current obs_vista 22.0.0-1   # run once
setup obs_vista                              # run in every shell
```

Running 

```Shell
eups list
```

Should show the 22.0.0-1 version of obs_vista as current and setup. Check the setup has worked by running

```Shell
butler create data                                      # Initiates Butler in data folder
butler register-instrument data lsst.obs.vista.VIRCAM   # Will only register VIRCAM instrument if obs_vista has been setup correctly
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

We are maintaining generation 2 functionality so that the first prototype runs remain accessible. This functionality should be deprecated around the start of 2022 following which we will delete all the generation 2 prototype data. If in doubt use the generation 3 Butler.


## The Camera

The package is designed to work with all VISTA data products. 
We are using the stacked images made by the VISTA pipeline so the camera definition is which is identical to the true camera geometry, is later modified to correct for different image dimensions in the stacked exposures.
The calibration of the VIRCAM instrument on the ESO VISTA telescope is described in [González-Fernández et al. 2018](https://ui.adsabs.harvard.edu/abs/2018MNRAS.474.5459G/abstract)

There is also further information on the VISTA technical specifications on the CASU website http://casu.ast.cam.ac.uk/surveys-projects/vista/technical

The notebook [camera/1_Build_detectors.ipynb](camera/1_Build_detectors.ipynb) is used to create the camera definition. In the generation 3 package this is stored in a single yaml file: [camera/vircam.yaml](camera/vircam.yaml).


---

## License

Copyright 2019 University of Southampton

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
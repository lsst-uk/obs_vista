# obs_vista
VISTA (VIRCAM) specific configuration and tasks for the LSST Data Management Stack. It describes the camera and data products, allowing the LSST stack to import and manipulate the data.

## Overview

This code is a modification of the obs_necam "Any cam" template; https://github.com/jrmullaney/obs_necam

The documenttation for this is at https://lsstcamdocs.readthedocs.io/en/latest/intro.html This documentation was developed during production of the obs package for the GOTO telescope.

As a first pass we have simply replaced Necam with VISTA throughout.

Folders:

- [camera](camera) Files containing information that describe the properties of VIRCAM (dimensions, gain etc).
- [config](config) Configuration files that tell the various stack process that access your data how to behave.
- [policy](policy) Files describing the file structure and type of input and output data (e.g., image, table etc).
- [python/lsst](python/lsst) This is where all the scripts go that manipulate VISTA data
- [ups](ups) A file telling the [eups](https://developer.lsst.io/stack/eups-tutorial.html) system what other packages need to be set up to use this obs_package.

## The Camera

The package is designed to work with all VISTA data products. The calibration of the
VIRCAM instrument on the ESO VISTA telescope is described in González-Fernández et al. 2018 https://ui.adsabs.harvard.edu/abs/2018MNRAS.474.5459G/abstract

## TODO

1. Specify file naming scheme used in the raw VISTA databases.

2. Define VISTA filters.

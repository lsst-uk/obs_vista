# Software Management Plan for the LSST IR fusion project

## What software will you develop?
- We will develop a software package enabling images from the VISTA telescope to be processed by the LSST Science Pipelines
- Crucially the code will allow the VISTA imaging to be processed alongside LSST optical imaging 

## Who are the intended users of your software?
- Research astronomers of all levels of experience who will want to access the resultant tables and images using the same protocols as for the the LSST data itself.
- Advanced users familiar with the LSST Science Pipelines who will run the code when LSST data is available and possibly alter configuration settings.

## How will you make your software available to your users?
- We will make all code available on GitHub on the LSST:UK organisation. We use the recommended Apache 2.0 license.
- Actual versions used for processing will be available alongside the full data sets.

## How will you support those who use your software?
- We will provide installation instructions and information about running the software.
- We encourage users to submit GitHub issues in the case of any bugs found.
- We will provide example code for accessing the data sets.
- We will maintain involvement with the LSST Community site in case of questions from users.

## How will your software contribute to research?
- The results of the software will be new data sets allowing users to attain near infrared photometry for associated LSST detected objects.
- The addition of VISTA fluxes will improve photometric redshifts and SED modelling for multiple science cases including AGN and galaxy formation.

## How will your software relate to other research objects?
- The datasets produced will be used by various research projects.
- NIR photometry will be useful to extragalactic science in general and will relate to 

## How will you measure your software's contribution to research?
- We will publish a paper documenting the test data set. The citation metrics will demonstrate how widely used the software is.

## Where will you deposit your software to guarantee its long-term availability?
- All code is held on the third party GitHub service, which we expect will persist for the long term, due to the volume of important software that it hosts.
- An installed version of the LSST Science Pipelines with the installed obs_vista code will be in place on IRIS allowing future developers to access the data reduction outputs using the exact version used to create it.
The obs_vista package
=====================================

The obs_vista pacage allows the LSST stack to interact with VISTA imaging.

To install you must first install the LSST Science Pipelines.
Following that you must make a directory inside the stack directory and declare and setup the package.
 
Following installation you should test the package using the small example in the database.
In order to run this you will need the minimal data set provided in an upcoming repository.
 
Installation notes
==================

Version 21:

In version 21 we needed to modify the following file:

/meas_modelfit/21.0.0+226a441f5f/python/lsst/meas/modelfit/cmodel/cmodelContinued.py

We commented out the WCS code in CModelForcedPlugin.measure. 
This should be removed in future versions.


.. toctree::
   :maxdepth: 2
 



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

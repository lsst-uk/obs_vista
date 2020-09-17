# Config overrides for converting gen2 to gen3 repos.

from lsst.obs.vista.ingest import VistaRawIngestTask

# Use the specialized Vista ingest task to handle multi-HDU FITS files.
config.raws.retarget(VistaRawIngestTask)
config.ccdKey = "ccd"
config.instrument = "lsst.obs.decam.Vista"
print("covertRepo.py run")
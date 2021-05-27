# Config overrides for converting gen2 to gen3 repos.

from lsst.obs.vista.ingest import VistaRawIngestTask

# Use the specialized Vista ingest task to handle multi-HDU FITS files.
config.raws.retarget(VistaRawIngestTask)
config.ccdKey = "ccdnum"
config.instrument = "lsst.obs.vista.VIRCAM"
print("covertRepo.py run")
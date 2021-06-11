#import os.path

#from lsst.obs.base.gen2to3 import ConvertRepoSkyMapConfig
from lsst.obs.vista import VISTA
from lsst.obs.vista.translators import VistaTranslator

maskCollection = VISTA().makeCollectionName("masks")
#config.runsForced["brightObjectMask"] = maskCollection
#config.extraUmbrellaChildren.append(maskCollection)
#config.skyMaps["vista_rings_v1"] = ConvertRepoSkyMapConfig()
#config.skyMaps["vista_rings_v1"].load(os.path.join(os.path.dirname(__file__), "makeSkyMap.py"))
# If there's no skymap in the root repo, but some dataset defined on
# tracts/patches is present there (i.e. brightObjectMask), assume this
# skymap.
#config.rootSkyMapName = "vista_rings_v1"

config.refCats.append("ps1_pv3_3pi_20170110_vista")

# ForcedPhotCoadd writes its configs to a filename that doesn't include a
# coaddName prefix, which means the conversion tools can't infer the right
# dataset type from the filename alone.  Because the vast majority of HSC coadd
# processing is on "deep" coadds, we explicitly ignore the other
# <prefix>Coadd_forced_config datasets.  Users who know what is in their own
# repositories can of course override.
#config.datasetIgnorePatterns.extend(["dcrCoadd_forced_config",
#                                     "goodSeeingCoadd_forced_config",
#                                     "psfMatchedCoadd_forced_config"])
# Same problem, with assembleCoadd variant metadata; we assume
# "deep_compareWarpAssembleCoadd_metadata" is the one we want.
#config.datasetIgnorePatterns.extend(["deep_assembleCoadd_metadata",
#                                     "deep_safeClipAssembleCoadd_metadata",
#                                     "deep_dcrAssembleCoadd_metadata",])



from lsst.obs.vista.ingest import VistaRawIngestTask

# Use the specialized Vista ingest task to handle multi-HDU FITS files.
config.raws.retarget(VistaRawIngestTask)
config.ccdKey = "ccdnum"
#config.instrument = VISTA
translatorClass= VistaTranslator
print("covertRepo.py run")

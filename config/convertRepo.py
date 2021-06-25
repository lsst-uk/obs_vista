import os.path

from lsst.obs.base.gen2to3 import ConvertRepoSkyMapConfig
from lsst.obs.vista import VISTA
from lsst.obs.vista.translators import VistaTranslator

#maskCollection = VISTA().makeCollectionName("masks")
#config.runsForced["brightObjectMask"] = maskCollection
#config.extraUmbrellaChildren.append(maskCollection)
#config.skyMaps["vista_rings_v1"] = ConvertRepoSkyMapConfig()
#config.skyMaps["vista_rings_v1"].load(os.path.join(os.path.dirname(__file__), "makeSkyMap.py"))
# If there's no skymap in the root repo, but some dataset defined on
# tracts/patches is present there (i.e. brightObjectMask), assume this
# skymap.
#config.rootSkyMapName = "vista_rings_v1"

#config.refCats.append("ps1_pv3_3pi_20170110")
#config.fgcmLoadReferenceCatalog.refObjLoader.ref_dataset_name = 'ps1_pv3_3pi_20170110'
#config.fgcmLoadReferenceCatalog.refObjLoader.ref_dataset_name = 'ps1_pv3_3pi_20170110'
#hscConfigDir = os.path.join(os.path.dirname(__file__))
#config.fgcmLoadReferenceCatalog.load(os.path.join(vistaConfigDir, 'filterMap.py'))
#config.fgcmLoadReferenceCatalog.applyColorTerms = True
#config.fgcmLoadReferenceCatalog.colorterms.load(os.path.join(vistaConfigDir, 'colorterms.py'))
#config.fgcmLoadReferenceCatalog.referenceSelector.doSignalToNoise = True
# Choose reference catalog signal-to-noise based on the PS1 i-band.
#config.fgcmLoadReferenceCatalog.referenceSelector.signalToNoise.fluxField = 'i_flux'
#config.fgcmLoadReferenceCatalog.referenceSelector.signalToNoise.errField = 'i_fluxErr'
# Minimum signal-to-noise cut for a reference star to be considered a match.
#config.fgcmLoadReferenceCatalog.referenceSelector.signalToNoise.minimum = 10.0
#config.defineVisits.load(os.path.join(os.path.dirname(__file__), "defineVisits.py"))
#config.connections.refCat = 'ps1_pv3_3pi_20170110'
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
config.datasetIgnorePatterns.extend(["deep_compareWarpAssembleCoadd_metadata",
                                     "deep_safeClipAssembleCoadd_metadata",
                                     "deep_dcrAssembleCoadd_metadata",
                                      ".DS_Store" ])



from lsst.obs.vista.ingest import VistaRawIngestTask

# Use the specialized Vista ingest task to handle multi-HDU FITS files.
#config.raws.retarget(VistaRawIngestTask)
config.ccdKey = "ccdnum"
#config.instrument = VISTA
translatorClass= VistaTranslator
print("covertRepo.py run")

import os.path

config_dir = os.path.dirname(__file__)

config.measurement.load(os.path.join(config_dir, "apertures.py"))
config.measurement.load(os.path.join(config_dir, "kron.py"))
config.measurement.load(os.path.join(config_dir, "convolvedFluxes.py"))
config.measurement.load(os.path.join(config_dir, "gaap.py"))
config.load(os.path.join(config_dir, "cmodel.py"))

config.measurement.slots.gaussianFlux = None

config.catalogCalculation.plugins.names = [
    "base_ClassificationExtendedness"
]
config.measurement.slots.psfFlux = "base_PsfFlux"


def doUndeblended(config, algName, fluxList=None):
    """Activate undeblended measurements for an algorithm."""
    if algName not in config.measurement.plugins:
        return

    if fluxList is None:
        fluxList = [algName + "_flux"]

    config.measurement.undeblended.names.add(algName)
    config.measurement.undeblended[algName] = \
        config.measurement.plugins[algName]

    for flux in fluxList:
        config.applyApCorr.proxies["undeblended_" + flux] = flux


doUndeblended(config, "base_PsfFlux")
doUndeblended(config, "ext_photometryKron_KronFlux")

doUndeblended(
    config,
    "base_CircularApertureFlux",
    [],
)

doUndeblended(
    config,
    "ext_convolved_ConvolvedFlux",
    config.measurement.plugins[
        "ext_convolved_ConvolvedFlux"
    ].getAllResultNames(),
)

doUndeblended(
    config,
    "ext_gaap_GaapFlux",
    config.measurement.plugins[
        "ext_gaap_GaapFlux"
    ].getAllGaapResultNames(),
)

config.measurement.undeblended[
    "ext_convolved_ConvolvedFlux"
].registerForApCorr = False

config.measurement.undeblended[
    "ext_gaap_GaapFlux"
].registerForApCorr = False

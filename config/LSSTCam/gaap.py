import lsst.meas.extensions.gaap  # noqa: F401 required to use GaapFlux below

config.plugins.names.add("ext_gaap_GaapFlux")

config.plugins["ext_gaap_GaapFlux"].sigmas = [
    0.5, 0.7, 1.0, 1.5, 2.5, 3.0
]

# Enable PSF photometry after PSF-Gaussianization.
config.plugins["ext_gaap_GaapFlux"].doPsfPhotometry = True

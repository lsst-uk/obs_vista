# Enable measurement of convolved fluxes
# 'config' is a SourceMeasurementConfig
try:
    import lsst.meas.extensions.convolved  # noqa: F401 required to use ConvolvedFlux below
except ImportError as exc:
    print("Cannot import lsst.meas.extensions.convolved (%s): disabling convolved flux measurements" % (exc,))
else:
    config.plugins.names.add("ext_convolved_ConvolvedFlux")
    # This target seeing is larger than any expected seeing in the coadd,
    # and so we'll always get a useful result.
    config.plugins["ext_convolved_ConvolvedFlux"].seeing.append(8.0)

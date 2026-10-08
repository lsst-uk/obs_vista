# Disable visit-level pointing refit for VIRCAM.
# The v30 refit rejects the VIRCAM detector pointings and can leave
# no valid target WCS for the visit.

config.do_refit_pointing = False
config.do_write_visit_geometry = False

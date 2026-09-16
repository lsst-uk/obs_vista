# Mapping of image filter/band names to reference-catalogue filter names.
# Appropriate for the Monster catalogue augmented with VIRCAM photometry.

for source, target in [
    ("VIRCAM-Z",  "z2"),
    ("VIRCAM-Y",  "y2"),
    ("VIRCAM-J",  "j"),
    ("VIRCAM-H",  "h"),
    ("VIRCAM-Ks", "ks"),

    ("Z", "z2"),
    ("Y", "y2"),
    ("J", "j"),
    ("H", "h"),
    ("K", "ks"),
]:
    config.filterMap[source] = target

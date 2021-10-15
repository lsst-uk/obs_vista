# Calibrate uses this to load calibrators
# All names on right are used in the refcats
# All names on the left are names of image bands as physcial_filter or band
for source, target in [
    ('HSC-G', 'g'),
    ('HSC-R', 'r'),
    ('HSC-I', 'i'),
    ('HSC-Z', 'z'),
    ('HSC-Y', 'y'),
    ('VIRCAM-Z', 'z2'),
    ('VIRCAM-Y', 'y2'),
    ('VIRCAM-J', 'j'),
    ('VIRCAM-H', 'h'),
    ('VIRCAM-Ks', 'g'),
    ('Z', 'z2'),
    ('Y', 'y2'),
    ('J', 'j'),
    ('H', 'h'),
    ('K','g'),
]:
    config.filterMap[source] = target

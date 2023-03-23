# Calibrate uses this to load calibrators
# All names on right are used in the refcats
# All names on the left are names of image bands as physcial_filter or band
for source, target in [
    ('EXT-G', 'g'),
    ('EXT-R', 'r'),
    ('EXT-I', 'i'),
    ('EXT-Z', 'z'),
    ('EXT-Y', 'y'),
    ('VIRCAM-Z', 'z2'),
    ('VIRCAM-Y', 'y2'),
    ('VIRCAM-J', 'j'),
    ('VIRCAM-H', 'h'),
    ('VIRCAM-Ks', 'ks'),
    ('Z', 'z2'),
    ('Y', 'y2'),
    ('J', 'j'),
    ('H', 'h'),
    ('K','ks'),
]:
    config.filterMap[source] = target

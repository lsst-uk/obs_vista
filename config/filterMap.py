# From obs_goto. Do I need this?
# I think that the targets here do NOT refer to color terms.
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
    ('VIRCAM-Ks', 'ks')
]:
    config.filterMap[source] = target

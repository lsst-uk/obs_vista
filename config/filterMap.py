#From obs_goto. Do I need this?
#I think that the targets here do NOT refer to color terms.
for source, target in [
    ('HSC-G', 'g'), 
    ('HSC-R', 'r'), 
    ('HSC-I', 'i'), 
    ('HSC-Z', 'z'),
    ('HSC-Y', 'y'),
    ('VISTA-Z', 'z'),
    ('VISTA-Y', 'y'),
    ('VISTA-J', 'j'),
    ('VISTA-H', 'h'),
    ('VISTA-Ks', 'ks')
    ]:
    config.filterMap[source] = target
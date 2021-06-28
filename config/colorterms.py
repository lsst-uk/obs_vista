#colorterms = config.photoCal.colorterms
from lsst.pipe.tasks.colorterms import ColortermDict, Colorterm


config.data = {

    "ps1*": ColortermDict(data={
        # Names used by Exposure.getFilter() in Gen2.
        'g': Colorterm(primary="g", secondary="r", c0=0.005728, c1=0.061749, c2=-0.001125),
        'r': Colorterm(primary="r", secondary="i", c0=-0.000144, c1=0.001369, c2=-0.008380),
        # 'r2': Colorterm(primary="r", secondary="i", c0=-0.000032, c1=-0.002866, c2=-0.012638),
        'i': Colorterm(primary="i", secondary="z", c0=0.000643, c1=-0.130078, c2=-0.006855),
        # 'i2': Colorterm(primary="i", secondary="z", c0=0.001625, c1=-0.200406, c2=-0.013666),
        'z': Colorterm(primary="z", secondary="y", c0=-0.005362, c1=-0.221551, c2=-0.308279),
        'y': Colorterm(primary="y", secondary="z", c0=-0.002055, c1=0.209680, c2=0.227296),
        'z2': Colorterm(primary="z2", secondary="z2"),
        'y2': Colorterm(primary="y2", secondary="y2"),
        'j': Colorterm(primary="j", secondary="j"),
        'h': Colorterm(primary="h", secondary="h"),
        'ks': Colorterm(primary="ks", secondary="ks"),

        # Names used by data IDs in both Gen2 and Gen3, and
        # Exposure.getFilter() in Gen3 (data is the same).
        'HSC-G': Colorterm(primary="g", secondary="r", c0=0.005728, c1=0.061749, c2=-0.001125),
        'HSC-R': Colorterm(primary="r", secondary="i", c0=-0.000144, c1=0.001369, c2=-0.008380),
        # 'HSC-R2': Colorterm(primary="r", secondary="i", c0=-0.000032, c1=-0.002866, c2=-0.012638),
        'HSC-I': Colorterm(primary="i", secondary="z", c0=0.000643, c1=-0.130078, c2=-0.006855),
        # 'HSC-I2': Colorterm(primary="i", secondary="z", c0=0.001625, c1=-0.200406, c2=-0.013666),
        'HSC-Z': Colorterm(primary="z", secondary="y", c0=-0.005362, c1=-0.221551, c2=-0.308279),
        'HSC-Y': Colorterm(primary="y", secondary="z", c0=-0.002055, c1=0.209680, c2=0.227296),
        'VISTA-Z': Colorterm(primary="z2", secondary="z2"),
        'VISTA-Y': Colorterm(primary="y2", secondary="y2"),
        'VISTA-J': Colorterm(primary="j", secondary="j"),
        'VISTA-H': Colorterm(primary="h", secondary="h"),
        'VISTA-Ks': Colorterm(primary="ks", secondary="ks"),
    }),
}


# if 'vista' in ref_cat:
#    colorterms.data["ps1*"] = ColortermDict(data={
#    #####HSC COLOUR TERMS FROM obs_subaru
#    'HSC-G': Colorterm(primary="g", secondary="r",
#    c0=0.00730066, c1=0.06508481, c2=-0.01510570),
#    'HSC-R': Colorterm(primary="r", secondary="i",
#    c0=0.00279757, c1=0.02093734, c2=-0.01877566),
#    'HSC-I': Colorterm(primary="i", secondary="z",
#    c0=0.00166891, c1=-0.13944659, c2=-0.03034094),
#    'HSC-Z': Colorterm(primary="z", secondary="y",
#    c0=-0.00907517, c1=-0.28840221, c2=-0.00316369),
#    'HSC-Y': Colorterm(primary="y", secondary="z",
#    c0=-0.00156858, c1=0.14747401, c2=0.02880125),
#    'VISTA-Z': Colorterm(primary="z2", secondary="y2",
#    c0=0.0, c1=-0.0, c2=-0.0),
#    'VISTA-Y': Colorterm(primary="y2", secondary="z2",
#    c0=0.0, c1=0.0, c2=0.0),
#    'VISTA-J': Colorterm(primary="j", secondary="y",
#    c0=0.0, c1=0.0, c2=0.0),
#    'VISTA-H': Colorterm(primary="h", secondary="y",
#    c0=0.0, c1=0.0, c2=0.0),
#    'VISTA-Ks': Colorterm(primary="ks", secondary="y",
#    c0=0.0, c1=0.0, c2=0.0),
# })
# elif ref_cat.endswith('2mass'):
#    colorterms.data["ps1*"] = ColortermDict(data={
#    #####HSC COLOUR TERMS FROM obs_subaru
#    'HSC-G': Colorterm(primary="g", secondary="r",
#    c0=0.00730066, c1=0.06508481, c2=-0.01510570),
#    'HSC-R': Colorterm(primary="r", secondary="i",
#    c0=0.00279757, c1=0.02093734, c2=-0.01877566),
#    'HSC-I': Colorterm(primary="i", secondary="z",
#    c0=0.00166891, c1=-0.13944659, c2=-0.03034094),
#    'HSC-Z': Colorterm(primary="z2", secondary="y2",
#    c0=-0.00907517, c1=-0.28840221, c2=-0.00316369),
#    'HSC-Y': Colorterm(primary="y2", secondary="z2",
#    c0=-0.00156858, c1=0.14747401, c2=0.02880125),
#    ####2MASS COLOUR TERMS - all from J, Ks - see above
#    'VISTA-Z': Colorterm(primary="j", secondary="ks",
#    c0=0.502-0.004, c1=0.86, c2=-0.0),
#    'VISTA-Y': Colorterm(primary="j", secondary="ks",
#    c0=0.600+0.022, c1=0.46, c2=0.0),
#    'VISTA-J': Colorterm(primary="j", secondary="ks",
#    c0=0.916, c1=0.031, c2=0.0),
#    'VISTA-H': Colorterm(primary="h", secondary="j",
#    c0=1.366-0.019, c1=0.032, c2=0.0),
#    'VISTA-Ks': Colorterm(primary="ks", secondary="j",
#    c0=1.827+0.011, c1=0.006, c2=0.0), #Sign inverted from form above
# })
# For the HSC r2 and i2 filters, use the r and i values from the catalog
# for refObjLoader in (config.calibrate.astromRefObjLoader,
#                      config.calibrate.photoRefObjLoader,
#                      config.charImage.refObjLoader,
#                      ):
#     pass
#    refObjLoader.filterMap['r2'] = 'r'
###    refObjLoader.filterMap['i2'] = 'i'

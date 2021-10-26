from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# lambdaMin and lambda max are chosen to be where the filter rises above 1%
# from HELP/SVO:
# https://github.com/H-E-L-P/herschelhelp_python/blob/master/database_builder/filters/
VIRCAM_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(band="Clear", physical_filter="NONE", lambdaEff=0,
                     alias=["Clear", "NONE", "None", "Unrecognised", "UNRECOGNISED",
                            "Unrecognized", "UNRECOGNIZED", "NOTSET"]),
    FilterDefinition(physical_filter="VIRCAM-Z",
                     band='Z',
                     lambdaEff=8762.4437058376E-1,
                     lambdaMin=8156.5423076923E-1,
                     lambdaMax=9400.45E-1),
    FilterDefinition(physical_filter="VIRCAM-Y",
                     band='Y',
                     lambdaEff=10184.228370757E-1,
                     lambdaMin=9427.060857538E-1,
                     lambdaMax=10976.565495208E-1),
    FilterDefinition(physical_filter="VIRCAM-J",
                     band='J',
                     lambdaEff=12464.429377059E-1,
                     lambdaMin=11427.444047011E-1,
                     lambdaMax=13759.028571429E-1),
    FilterDefinition(physical_filter="VIRCAM-H",
                     band='H',
                     lambdaEff=16310.014908445E-1,
                     lambdaMin=14603.599766628E-1,
                     lambdaMax=18422.112893276E-1),
    FilterDefinition(physical_filter="VIRCAM-Ks",
    #K Capitalised and without s based on
    #https://github.com/lsst/skymap/blob/master/python/lsst/skymap/packers.py
                     band="K", 
                     lambdaEff=21336.637909756E-1,
                     lambdaMin=19332.653810836E-1,
                     lambdaMax=23674.330024814E-1),
    # Copy pasted from obs_subaru. 
    # Hopefully gen 3 will allow these to be used directly from obs_subaru
    FilterDefinition(physical_filter="HSC-G",
                     band="g",
                     lambdaEff=477, alias={'W-S-G+'}),
    FilterDefinition(physical_filter="HSC-R",
                     band="r",
                     lambdaEff=623, alias={'W-S-R+'}),
    FilterDefinition(physical_filter="HSC-I",
                     band="i",
                     lambdaEff=775, alias={'W-S-I+'}),
    FilterDefinition(physical_filter="HSC-Z",
                     band="z",
                     lambdaEff=925, alias={'W-S-Z+'}),
    FilterDefinition(physical_filter="HSC-Y",
                     band="y",
                     lambdaEff=990, alias={'W-S-ZR'}),
)

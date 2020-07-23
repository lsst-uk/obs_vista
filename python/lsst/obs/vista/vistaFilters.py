from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# lambdaMin and lambda max are chosen to be where the filter rises above 1%
# from HELP/SVO:
#https://github.com/H-E-L-P/herschelhelp_python/blob/master/database_builder/filters/
VISTA_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(physical_filter="VISTA-z",
                     abstract_filter="z",
                     lambdaEff=8762.4437058376, 
                     lambdaMin=8156.5423076923, 
                     lambdaMax=9400.45),
    FilterDefinition(physical_filter="VISTA-Y",
                     abstract_filter="y",
                     lambdaEff=10184.228370757, 
                     lambdaMin=9427.060857538, 
                     lambdaMax=10976.565495208),
    FilterDefinition(physical_filter="VISTA-J",
                     abstract_filter="j",
                     lambdaEff=12464.429377059, 
                     lambdaMin=11427.444047011, 
                     lambdaMax=13759.028571429),
    FilterDefinition(physical_filter="VISTA-H",
                     abstract_filter="h",
                     lambdaEff=16310.014908445, 
                     lambdaMin=14603.599766628, 
                     lambdaMax=18422.112893276),
    FilterDefinition(physical_filter="VISTA-Ks",
                     abstract_filter="k",
                     lambdaEff=21336.637909756, 
                     lambdaMin=19332.653810836, 
                     lambdaMax=23674.330024814),

)
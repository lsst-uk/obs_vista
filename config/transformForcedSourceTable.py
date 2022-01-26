import os

# Use the environment variable to prevent hardcoding of paths
# into quantum graphs.
ObsConfigDir = os.path.dirname(__file__)
config.functorFile = os.path.join(ObsConfigDir.replace('config','policy'), 'ForcedSource.yaml')

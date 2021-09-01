import os.path
# Gen3 mergeDetections will supersede mergeCoaddDetections
# Keep in sync in the meantime
config.load(os.path.join(os.path.dirname(__file__), "mergeDetections.py"))
# config.priorityList = [
#     "HSC-I",
#     "HSC-R",
#     "HSC-Z",
#     "HSC-Y",
#     "HSC-G",
#     "VIRCAM-Z",
#     "VIRCAM-Y",
#     "VIRCAM-J",
#     "VIRCAM-H",
#     "VIRCAM-Ks"
# ]

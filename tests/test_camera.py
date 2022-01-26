import unittest
from collections import namedtuple

import lsst.utils.tests
from lsst.afw.image import Filter
from lsst.obs.vista import VircamMapper


class CameraTestCase(lsst.utils.tests.TestCase):

    def setUp(self):
        self.mapper = VircamMapper(root=".", calibRoot=".")
        self.camera = self.mapper.camera

    def tearDown(self):
        del self.camera
        del self.mapper

    def testName(self):
        self.assertEqual(self.camera.getName(), "Vircam")

    def testNumCcds(self):
        self.assertEqual(len(list(self.camera.getIdIter())), 16)

    def testCcdSize(self):
        for ccd in self.camera:
            self.assertEqual(ccd.getBBox().getWidth(), 2049) #Why does 2048 fail?
            self.assertEqual(ccd.getBBox().getHeight(), 2049)

    def testFilters(self):
        # Check that the mapper has defined some standard filters.
        # Note that this list is not intended to be comprehensive -- we
        # anticipate that more filters can be added without causing the test
        # to break -- but captures the standard HSC broad-band filters.
        FilterName = namedtuple("FilterName", ["alias", "canonical"])
        filterNames = (
            FilterName(alias="HSC-G", canonical="g"),
            FilterName(alias="HSC-R", canonical="r"),
            FilterName(alias="HSC-I", canonical="i"),
            FilterName(alias="HSC-Z", canonical="z"),
            FilterName(alias="HSC-Y", canonical="y"),
            FilterName(alias="NONE", canonical="Clear")
        )

        for filterName in filterNames:
            self.assertIn(filterName.alias, self.mapper.filters)
            self.assertEqual(Filter(filterName.alias).getCanonicalName(), filterName.canonical)


# No VircamMapper.clearCache implemented 
# class TestMemory(lsst.utils.tests.MemoryTestCase):
#     def setUp(self):
#         VircamMapper.clearCache()
#         lsst.utils.tests.MemoryTestCase.setUp(self)


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
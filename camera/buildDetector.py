import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is copying from afw/tests/testAmpInfoTable.py:
readout = [[20.]]
gain_all = [[0.5]]

# As a first pass hack I am just taking an HSC example fits file and modifying pixel numbers. I do this in a notebook in docs
# TODO: specify all the detector definitions here.


def addAmp(ampCatalog, i, rN, gain_s):
    record = ampCatalog.addNew()

    width = 2048
    height = 2048

    os = 0  # pixels of overscan

    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width, height))
    bbox.shift(afwGeom.Extent2I(width*i, 0))

    gain = gain_s
    saturation = 65535
    readNoise = rN
    readoutCorner = afwTable.LL if i == 0 else afwTable.LR
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width, height))
    rawXYOffset = afwGeom.Extent2I(0, 0)
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(0 if i == 0 else 0, 0), afwGeom.Extent2I(width, height))
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(
        0 if i == 0 else width-os-1, 0), afwGeom.Extent2I(os, 6220))
    #rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(50, 6132), afwGeom.Extent2I(0, 0))
    #rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))
    emptyBox = afwGeom.BoxI()

    shiftp = afwGeom.Extent2I((width)*i, 0)
    rawBBox.shift(shiftp)
    rawDataBBox.shift(shiftp)
    rawHorizontalOverscanBBox.shift(shiftp)

    record.setHasRawInfo(True)  # Sets the first Flag=True
    record.setRawFlipX(False)  # Sets the second Flag=False
    record.setRawFlipY(False)  # Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left' if i == 0 else 'right')
    record.setGain(gain)
    record.setSaturation(saturation)
    record.setReadNoise(readNoise)
    record.setReadoutCorner(readoutCorner)
    record.setLinearityCoeffs(linearityCoeffs)
    record.setLinearityType(linearityType)
    record.setRawBBox(rawBBox)
    record.setRawXYOffset(rawXYOffset)
    record.setRawDataBBox(rawDataBBox)
    record.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    record.setRawVerticalOverscanBBox(emptyBox)
    record.setRawPrescanBBox(emptyBox)


def makeCcd(ccdId):
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    ccdName = ccdId+1
    for i in range(1):
        addAmp(ampCatalog, i, readout[ccdId-1][i], gain_all[ccdId-1][i])
    return ampCatalog.writeFits('n%s_vista.fits' % ccdName)


def main():
    for i in range(1):
        camera = makeCcd(i)


if __name__ == "__main__":
    main()

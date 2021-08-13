from lsst.pipe.tasks.ingest import ParseTask, IngestTask, IngestArgumentParser
import lsst.obs.base
from lsst.obs.base.ingest import RawFileData
from lsst.afw.fits import readMetadata
import lsst.obs.base.RawIngestTask
import lsst.afw.fits.Fits 

from ._instrument import VIRCAM

# We need to write a VISTA translator for the gen3 butler
#from astro_metadata_translator import fix_header

import os
import re

from astropy.time import Time

__all__ = [
    "VircamRawIngestTask",
    "VistaIngestArgumentParser",
    "VistaIngestTask",
    "VistaParseTask"
]


# This should eventually be deprecated
#We still need it while the translator is not in astro_meta_data_translator
class VircamRawIngestTask(lsst.obs.base.RawIngestTask):
    """Task for ingesting raw VISTA data into a Gen3 Butler repository.

    Function copied from obs_decam DecamRawIngestTask which also has fits files
    with multiple extensions.

    This is now deprecated and they use the default ingester.

    We need to write an astro_metadata_translator for VISTA to use this with the gen3
    butler
    """

    def extractMetadata(self, filename: str) -> RawFileData:
        datasets = []
        print(filename)
        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            header = fitsData.readMetadata()

            # if header['ESO DET CHIP NO'] > 16:
            #    continue
            # fix_header(header) #needs astro_metadata_translator for VISTA
            datasets.append(self._calculate_dataset_info(header, filename))

        # The data model currently assumes that whilst multiple datasets
        # can be associated with a single file, they must all share the
        # same formatter.
        instrument = VIRCAM()
        FormatterClass = instrument.getRawFormatter(datasets[0].dataId)

        self.log.debug(f"Found images for {len(datasets)} detectors in {filename}")
        return RawFileData(datasets=datasets, filename=filename,
                           FormatterClass=FormatterClass,
                           instrumentClass=type(instrument))


class VistaIngestArgumentParser(IngestArgumentParser):
    """Gen2 Vista ingest additional arguments.
    """

    def __init__(self, *args, **kwargs):
        super(VistaIngestArgumentParser, self).__init__(*args, **kwargs)
        # We might eventually want to be able to go straight from the raw exposures or
        # the CASU calibrated ones, or the pointing stacks, or the full tiles
        self.add_argument(
            "--filetype", default="raw",
            choices=["raw", "instcal", "stack", "tile", "hsc_calexp"],
            help="Data processing level of the files to be ingested")


class VistaIngestTask(IngestTask):
    """Gen2 VISTA file ingest task.
    """
    ArgumentParser = VistaIngestArgumentParser

    def __init__(self, *args, **kwargs):
        super(VistaIngestTask, self).__init__(*args, **kwargs)

    def run(self, args):
        """Ingest all specified files and add them to the registry
        """

        if args.filetype == "raw":
            IngestTask.run(self, args)

        elif args.filetype == "instcal":
            root = args.input
            with self.register.openRegistry(
                root, create=args.create, dryrun=args.dryrun
            ) as registry:
                for infile in args.files:

                    fileInfo, hduInfoList = self.parse.getInfo(infile, args.filetype)
                    if len(hduInfoList) > 0:
                        outfileStack = os.path.join(
                            root,
                            self.parse.getDestination(
                                args.butler,
                                hduInfoList[0],
                                infile, "instcal"
                            )
                        )
                        ingestedStack = self.ingest(
                            fileInfo["instcal"], outfileStack,
                            mode=args.mode, dryrun=args.dryrun
                        )

                        if not ingestedStack:
                            continue

                    for info in hduInfoList:
                        self.register.addRow(
                            registry, info, dryrun=args.dryrun, create=args.create
                        )


class VistaParseTask(ParseTask):

    '''
    [From https://github.com/lsst/obs_lsst/blob/f0c4ae506e8e0a85789aebdd970d7e704c9c6e24/
    python/lsst/obs/lsst/ingest.py#L54]:
    All translator methods receive the header metadata [here via "md"] and should return the appropriate value, or None if the value cannot be determined.

    How does it deal with extensions?

    Here we define the functions required to translate the VISTA metadata into the 
    standard required by the LSST stack. It will work with the header keys defined in 
    config/ingest.py
    '''
    # Why a new zero point? To save bits?
    # DAY0 = 55927  # Zero point for  2012-01-01  51544 -> 2000-01-01

    def __init__(self, *args, **kwargs):
        super(ParseTask, self).__init__(*args, **kwargs)

        self.expnumMapper = None

        # Note that these should be syncronized with the fields in
        # root.register.columns defined in config/ingest.py
        self.instcalPrefix = "instcal"
        self.confPrefix = "conf"
        self.catPrefix = "cat"

    def translateDataType(self, md):
        '''Convert dtype header

        What is data type? Science vs flat or float vs int arrays?
        '''
        return md.get("XTENSION")

    def translateFilter(self, md):
        '''Takes VISTA filter name and converts it

        '''
        # Find a better way to get the filter - access to top level header?
        # e.g. turn 'Done with sky_20180911_266_Y.fit[1]' to 'Y'
        # _st.fit stack files
        try:
            filter = 'VIRCAM-'+md.get("SKYSUB").split('.')[0][-1]
            if filter == 'VIRCAM-s':
                filter = 'VIRCAM-Ks'

        except:
            filter = 'Clear'  # +md.get("ESO INS FILT1 NAME")

        # [0-9].fit single exposures
        try:
            filter = self.filter
            if filter == 'VIRCAM-s':
                filter = 'VIRCAM-Ks'
        except:
            filter = 'Clear'  # +md.get("ESO INS FILT1 NAME")

        return filter

    def translateNumObs(self, md):
        '''Get numObs from filename parsed to local variable'''
        try:
            numObs = self.numObs
        except:
            numObs = '0'
        return numObs

    def translateDataType(self, md):
        '''Get data type (stack or exposure) from filename parsed to local variable'''
        try:
            dataType = self.dataType
        except:
            dataType = 'unknown'
        return dataType

    def translateDate(self, md):
        '''
        This strips everything apart form yyyy-mm-dd
        '''
        date = md.get("DATE-OBS")
        # print(date,type(date))
        start = date[11:]
        date = date[0:10]

        t = Time(date)
        # If after midnight, set date to date minus 1 day.
        if int(start.split(":")[0]) < 12:
            date = Time(t.jd-1, format='jd').isot

        # print('d'+date)
        return date[0:10]

    def translateTai(self, md):
        '''
        This gives the full iso time
        '''
        t = Time(md.get("DATE-OBS"), format='isot')
        # print('tai:'+t.isot)
        return t.isot

    def translateJd(self, md):
        date = self.translateDate(md)
        # print(date)
        t = Time(date, format='isot')
        # print(int(t.mjd))
        return int(t.mjd)  # - self.DAY0

    def translateCcd(self, md):
        '''
        Header information is extracted as string, but "ccd" is more suited to integer.

        This seems to give access to the extensions directly. Does this need to return 
        the form of CCD name used in camera?
        '''
        # take e.g. 'DET1.CHIP12' and return the integer 11 (we use 0 indexing)
        # This seems to be just taking the first extension
        #ccd = int(md.get("EXTNAME")[9:]) - 1
        ccd = int(md.get("ESO DET CHIP NO"))
        return ccd

    def getInfo(self, filename, filetype="raw"):
        """Get metadata header info from multi-extension FITS decam image file.

        The science pixels, mask, and weight (inverse variance) are
        stored in separate files each with a unique name but with a
        common unique identifier EXPNUM in the FITS header.  We have
        to aggregate the 3 filenames for a given EXPNUM and return
        this information along with that returned by the base class.

        This appears to be the only way to use the filename.

        Parameters
        ----------
        filename : `str`
            Image file to retrieve info from.
        filetype : `str`
            One of "raw" or "instcal".

        Returns
        -------
        phuInfo : `dict`
            Primary header unit info.
        infoList : `list` of `dict`
            Info for the other HDUs.

        Notes
        -----
        For filetype="instcal", we expect a directory structure that looks
        like the following:

        .. code-block:: none

            dqmask/
            instcal/
            wtmap/

        The user creates the registry by running:

        .. code-block:: none

            ingestImagesDecam.py outputRepository --filetype=instcal --mode=link instcal/*fits
        """

        if filetype == "raw":
            phuInfo, infoList = super(VistaParseTask, self).getInfo(filename)
            self.filter = 'VIRCAM-'+readMetadata(filename, 0).get('ESO INS FILT1 NAME')
            self.numObs = filename.split('/')[-1].split('_')[1].split('.')[0]
            self.dataType = 'exposure'
            if filename.endswith('_st.fit'):
                self.dataType = 'stack'
            phuInfo['filter'] = self.filter
            phuInfo['numObs'] = self.numObs
            phuInfo['dataType'] = self.dataType
            for info in infoList:
                #print("DEBUG raw loop" , info)
                info[self.instcalPrefix] = ""
                info[self.confPrefix] = ""
                info[self.catPrefix] = ""
                info['filter'] = self.filter
                info['numObs'] = self.numObs
                info['dataType'] = self.dataType

        elif filetype == "instcal":
            # if self.expnumMapper is None:
            #    self.buildExpnumMapper(os.path.dirname(os.path.abspath(filename)))

            # Note that phuInfo will have
            #   'side': 'X', 'ccd': 0
            phuInfo, infoList = super(VistaParseTask, self).getInfo(filename)
            expnum = phuInfo["visit"]
            phuInfo[self.instcalPrefix] = ""  # self.expnumMapper[expnum][self.instcalPrefix]
            phuInfo[self.confPrefix] = ""  # self.expnumMapper[expnum][self.confPrefix]
            phuInfo[self.catPrefix] = ""  # self.expnumMapper[expnum][self.catPrefix]
            for info in infoList:
                #print("DEBUG", info)
                expnum = info["visit"]
                info[self.instcalPrefix] = ""  # self.expnumMapper[expnum][self.instcalPrefix]
                info[self.confPrefix] = ""  # self.expnumMapper[expnum][self.confPrefix]
                info[self.catPrefix] = ""  # self.expnumMapper[expnum][self.catPrefix]

        # Some data IDs can not be extracted from the zeroth extension
        # of the MEF. Add them so Butler does not try to find them
        # in the registry which may still yet to be created.
        for key in ("ccdnum", "hdu", "ccd"):
            if key not in phuInfo:
                phuInfo[key] = 0

        return phuInfo, infoList

    @staticmethod
    def getExtensionName(md):
        return md.getScalar('EXTNAME')

    def getDestination(self, butler, info, filename, filetype="raw"):
        """Get destination for the file

        Parameters
        ----------
        butler : `lsst.daf.persistence.Butler`
            Data butler.
        info : data ID
            File properties, used as dataId for the butler.
        filename : `str`
            Input filename.

        Returns
        -------
        raw : `str`
            Destination filename.
        """
        self.filter = 'VIRCAM-'+readMetadata(filename, 0).get('ESO INS FILT1 NAME')
        self.numObs = filename.split('/')[-1].split('_')[1]
        raw = butler.get("%s_filename"%(filetype), info)[0]
        # Ensure filename is devoid of cfitsio directions about HDUs
        c = raw.find("[")

        if c > 0:
            raw = raw[:c]

        return raw

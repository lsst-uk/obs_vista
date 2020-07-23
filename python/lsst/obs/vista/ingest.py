from lsst.pipe.tasks.ingest import ParseTask, IngestTask, IngestArgumentParser
from astropy.time import Time
import lsst.obs.base    
    
    
__all__ = [
    "VistaRawIngestTask", 
    "VistaIngestArgumentParser", 
    "VistaIngestTask", 
    "VistaParseTask"
]
    
class VistaRawIngestTask(lsst.obs.base.RawIngestTask):
    """Task for ingesting raw VISTA data into a Gen3 Butler repository.
    
    Function copied from obs_decam DecamRawIngestTask which also has fits files
    with multiple extensions.
    """
    def extractMetadata(self, filename: str) -> RawFileData:
        datasets = []
        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            header = fitsData.readMetadata()
            if header['ESO DET CHIP NO'] > 16:  # ignore the guide CCDs#VISTA has these?
                continue
            fix_header(header)
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
        #We might eventually want to be able to go straight from the raw exposures or 
        # the CASU calibrated ones, or the pointing stacks, or the full tiles
        self.add_argument("--filetype", default="stack", choices=["stack", "raw"],
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
        if args.filetype == "stack":
            root = args.input
            with self.register.openRegistry(
                root, create=args.create, dryrun=args.dryrun
            ) as registry:
                for infile in args.files:
                    fileInfo, hduInfoList = self.parse.getInfo(infile, args.filetype)
                    if len(hduInfoList) > 0:
                        outfileSt = os.path.join(
                            root, 
                            self.parse.getDestination(
                                args.butler,
                                hduInfoList[0],
                                infile, 
                                "stack"
                            )
                        )
                        #outfileConf = os.path.join(
                        #    root, 
                        #    self.parse.getDestination(
                        #        args.butler,
                        #        hduInfoList[0], 
                        #        infile,
                        #        "conf"
                        #    )
                        #)


                        ingestedStack = self.ingest(fileInfo["stack"], outfileStack,
                                                      mode=args.mode, dryrun=args.dryrun)
                        #ingestedConf = self.ingest(fileInfo["conf"], outfileConf,
                        #                             mode=args.mode, dryrun=args.dryrun)


                        if not (
                            ingestedStack 
                            #or ingestedDqmask 
                        ):
                            continue

                    for info in hduInfoList:
                        self.register.addRow(
                            registry, 
                            info, 
                            dryrun=args.dryrun, 
                            create=args.create
                        )

        elif args.filetype == "raw":
            IngestTask.run(self, args)
            
    
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
    def translateDataType(self, md):
        '''Convert dtype header
        
        What is data type? Science vs flat or float vs int arrays?
        '''
        return md.get("XTENSION")
    
    def translateFilter(self, md):
        '''Takes VISTA filter name and converts it
        
        '''
        #Find a better way to get the filter - access to top level header?
        #e.g. turn 'Done with sky_20180911_266_Y.fit[1]' to 'Y'
        return 'VISTA-'+md.get("SKYSUB")[-8:-7]

    def translateDate(self, md):
        '''
        This strips everything apart form yyyy-mm-dd
        '''
        date = md.get("DATE-OBS")
        start = date[11:]
        date = date[0:10]
        
        t = Time(date)
        #If after midnight, set date to date minus 1 day.
        if int(start.split(":")[0]) < 12:
            date = Time(t.jd-1, format='jd', out_subfmt='date').iso
                
        return date
        
    def translateJd(self, md):
        date = self.translateDate(md)
        t = Time(date, format='iso')
        return int(t.mjd)
     
                    
    def translateCcd(self, md):
        '''
        Header information is extracted as string, but "ccd" is more suited to integer.
        
        This seems to give access to the extensions directly. Does this need to return 
        the form of CCD name used in camera?
        '''
        #take e.g. 'DET1.CHIP12' and return the integer 11 (we use 0 indexing)
        #This seems to be just taking the first extension
        #ccd = int(md.get("EXTNAME")[9:]) - 1
        ccd = md.get('ESO DET CHIP NO') -1
        return ccd

                

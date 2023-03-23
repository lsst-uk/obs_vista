
__all__ = ("VircamTranslator", )

from astro_metadata_translator import cache_translation, FitsTranslator
from astro_metadata_translator.translators.helpers import (
    tracking_from_degree_headers,altaz_from_degree_headers)
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, Angle, AltAz, EarthLocation
from astropy.io import fits
from astropy.wcs import WCS

class VircamTranslator(FitsTranslator):
    """Metadata translator for VISTA FITS headers.

    Under normal circumstances, translators are found in the astro_metadata_translator 
    repository. However, it is possible to also put them in an obs_package, provided that 
    they are imported in both the _instrument.py and rawFormatter.py files.

    This one is in obs_vista to keep everything togeter in one place.  
    """

    """Name of this translation class"""
    name = "VIRCAM"

    """Supports the VIRCAM instrument."""
    supported_instrument = "VIRCAM"

    """
    _const_map includes properties that you may not know, nor can calculate.
    
    Bear in mind that some examples listed here as "None" may require units or be a 
    specific class should you want to upgrade them to _trivial_map or to_<<example>>. 
    For example, "altaz_begin" needs to be an astropy.coordinates.AltAz class. 
    
    https://www.eso.org/sci/facilities/paranal/instruments/vircam/inst.html
    On the sky (in the default instrument rotator position) +Y corresponds to N, 
    and +X to West:
    """
    _const_map = {"boresight_rotation_coord": "sky",
                  "detector_group": None,
                  "boresight_airmass": None,  # This could be calculated.
                 # "boresight_rotation_angle": Angle(0 * u.deg),
                  "science_program": None,
                 # "temperature": 300. * u.K,
                  "pressure": 985. * u.hPa,
                  "relative_humidity": None,
                 # "altaz_begin": AltAz(0*u.deg,90*u.deg),  # This could be calculated.
                  #"location": None,
                  }

    """
    _trivial_map includes properties that can be taken directly from header
    """
    _trivial_map = {
        #"exposure_id": "ESO DET EXP NO",
        #"visit_id": "ESO DET EXP NO",
        #"temperature":("ESO INS THERMAL AMB MEAN", dict(unit=u.K)),
        #"boresight_airmass": ""
        "observation_id": "ESO DET EXP NO",
        #"detector_exposure_id": "ESO DET EXP NO",
        "detector_num": "ESO DET CHIP NO",
        "detector_serial": "ESO DET CHIP NO",
        # "physical_filter": "HIERARCH ESO INS FILT1 NAME",
        #"dithers": "ESO DET NDIT",
        "exposure_time": ("EXPTIME", dict(unit=u.s)),
        "dark_time": ("EXPTIME", dict(unit=u.s)),
        # This is a hack we need to merge to primary header
        "object": "ORIGIN",
        #"observation_type": "ESO DPR TYPE",
        "telescope": ("TELESCOP", dict(default="VISTA")),
        "instrument": ("INSTRUME", dict(default="VIRCAM")),
    }
    
#     detector_names = {
#         1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 
#         9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', }

    @classmethod
    def can_translate(cls, header, filename=None):
        """
        butler ingest-raws cycles through the known translators, using this method to 
        determine whether each one can translate supplied header. 

        This example just checks the INSTRUME header keyword and returns True if it 
        contains "VIRCAM". However, you can make this as stringent as you like (e.g., 
        perhaps you can currently handle a limited range of filters) 

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.
        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """

        # Use INSTRUME. Because of defaulting behavior only do this
        # if we really have an INSTRUME header

#         if "INSTRUME" in header:
# 
#             if header["INSTRUME"] == "VIRCAM":
# 
#                 return True
#         return False
        if "INSTRUME" in header:
            via_instrume = super().can_translate(header, filename=filename)
            if via_instrume:
                return via_instrume
#         if cls.is_keyword_defined(header, "FILTER") and "VIRCAM" in header["FILTER"]:
#             return True
        return False

    """
    The to_<<example>> methods are used when properties can't be trivially taken from the 
    header. 
    
    For example, the date in the header needs to be converted into an astropy.Time class.
    """
    @cache_translation
    def to_datetime_begin(self):

        date = self._header["DATE-OBS"]
        # print(date)
        #date = [date[0:4], date[4:6], date[6:]]
        #date = '-'.join(date)
        t = Time(date, format="isot", scale="utc")
        return t
        
    @cache_translation
    def to_boresight_rotation_angle(self):
        """"Give zero for typical pointing == -90deg"""
        #primary=fits.open(self.filename)[0]
        #posang=primary.header["HIERARCH ESO TEL POSANG"]
        posang=self._header["ESO TEL POSANG"]
        return Angle(-(posang + 90.)* u.deg) #+90?
        
#     @cache_translation
#     def to_boresight_airmass(self):
#         return self._header["ESO OBS AIRM "] # requested maximum - not available for stack

    @cache_translation
    def to_datetime_end(self):
        datetime_end = self.to_datetime_begin() + self.to_exposure_time()
        return datetime_end
    
    @cache_translation
    def to_temperature(self):

        #print(self._header)
#         primary=fits.open(self.filename)[0]
#         temp=primary.header["ESO INS THERMAL AMB MEAN"]*u.K
        temp=self._header["ESO INS THERMAL AMB MEAN"]*u.K
        return temp
        
    @cache_translation
    def to_tracking_radec(self):
        # Docstring will be inherited. Property defined in properties.py
        radecsys = ("RADECSYS",)
        radecpairs = (("CRVAL1", "CRVAL2"),)
        #print("FILENAME:",self.filename)
#         #return None
# 
# 
#         wcs_input_dict = {
#             'CTYPE1': self._header['CTYPE1'],
#             'CUNIT1': 'deg',
#             'CD1_1':  self._header['CD1_1'],                   
#             'CD1_2':  self._header['CD1_2'] ,                 
#             'CRPIX1': self._header['CRPIX1'],
#             'CRVAL1': self._header['CRVAL1'],
#             'NAXIS1': self._header['NAXIS1'],
#             
#             'CTYPE2': self._header['CTYPE2'],
#             'CUNIT2': 'deg',                
#             'CD2_1':  self._header['CD2_1'],                  
#             'CD2_2':  self._header['CD2_2'],
#             'CRPIX2': self._header['CRPIX2'],
#             'CRVAL2': self._header['CRVAL2'],
#             'NAXIS2': self._header['NAXIS2'],
#             'PV2_1':  self._header['PV2_1'],                 
#             'PV2_2':  self._header['PV2_2'],                      
#             'PV2_3':  self._header['PV2_3'],                       
#             'PV2_4':  self._header['PV2_4'],                      
#             'PV2_5':  self._header['PV2_5'], 
#         }
#         w = WCS(wcs_input_dict)
        #return w.pixel_to_world(0,0)
        #primary=fits.open(self.filename)[0]
        #c=SkyCoord(primary.header['RA'],primary.header['DEC'],unit='deg')
        #return c
        return tracking_from_degree_headers(self, radecsys, radecpairs, unit=u.deg)
#         return w.pixel_to_world(self._header['NAXIS1']/2,self._header['NAXIS2']/2)
#         print(self._header)
#         radecsys = ("RADECSYS",)
#         radecpairs = (("RA", "DEC"),)
#         return tracking_from_degree_headers(self, radecsys, radecpairs, unit=u.deg)
        
        

    @cache_translation
    #Not working possibly due to not being in extension header
    def to_altaz_begin(self):
        # Docstring will be inherited. Property defined in properties.py
#         primary=fits.open(self.filename)[0]
#         return AltAz(primary.header["ESO TEL AZ"]*u.deg,primary.header["ESO TEL ALT"]*u.deg)
         return altaz_from_degree_headers(self, (("ESO TEL ALT","ESO TEL AZ"),),
                                          self.to_datetime_begin(), 
                                          is_zd=set(["ESO TEL ALT"]))

    @cache_translation
    def to_physical_filter(self):
        """Calculate physical filter.
        We are reading the headers from the image layers of a multiextension fits
        Not from the primary HDU

        Returns
        -------
        filter : `str`
            The full filter name.
        """
        if self.is_key_ok("FILTER"):
            value = 'VIRCAM-{}'.format(self._header["FILTER"].strip())
            self._used_these_cards("FILTER")
            return value
        elif self.is_key_ok("FLATCOR"):
            value = 'VIRCAM-{}'.format(self._header["FLATCOR"].split('_')[0])
            self._used_these_cards("FLATCOR")
            return value
        else:
            return None
            
    @cache_translation
    def to_location(self):
        """Calculate the observatory location.
        Returns
        -------
        location : `astropy.coordinates.EarthLocation`
            An object representing the location of the telescope.
        """

        # Look up the value since files do not have location
        value = EarthLocation.of_site("paranal")

        return value

#     @cache_translation
#     def to_instrument(self):
#         if self._header["INSTRUME"].strip(" ") == "VIRCAM":
#             return "VIRCAM"
#         else:
#             # It should never get here, given can_translate().
#             return "Unknown"
# 
#     def to_telescope(self):
#         return self.to_instrument()
    @cache_translation
    def to_exposure_id(self):
        """Calculate exposure ID.
        Returns
        -------
        id : `int`
            ID of exposure.
        """
        value = self._header["ESO DET EXP NO"]
        self._used_these_cards("ESO DET EXP NO")
        return value

    @cache_translation
    def to_observation_counter(self):
        """Return the lifetime exposure number.
        Returns
        -------
        sequence : `int`
            The observation counter.
        """
        return self.to_exposure_id()

    @cache_translation
    def to_visit_id(self):
        # Docstring will be inherited. Property defined in properties.py
        return self.to_exposure_id()
        
    @cache_translation
    def to_detector_name(self):
        return '{:02d}'.format(self._header["ESO DET CHIP NO"])
#     @cache_translation
#     def to_detector_name(self):
#         # Docstring will be inherited. Property defined in properties.py
#         name = self.to_detector_unique_name()
#         return name[1:]

    @cache_translation
    def to_observation_type(self):
        return 'science'
        
    @cache_translation
    def to_detector_exposure_id(self):
        # Docstring will be inherited. Property defined in properties.py
        exposure_id = self.to_exposure_id()
        if exposure_id is None:
            return None
        return int("{:07d}{:02d}".format(exposure_id, self.to_detector_num()))

#     @cache_translation
#     def to_detector_group(self):
#         # Docstring will be inherited. Property defined in properties.py
#         name = self.to_detector_unique_name()
#         return name[0]

#     @cache_translation
#     def to_detector_name(self):
#         # Docstring will be inherited. Property defined in properties.py
#         name = self.to_detector_unique_name()
#         return name[1:]

    @classmethod
    def determine_translatable_headers(cls, filename, primary=None):
        """Given a file return all the headers usable for metadata translation.
        VIRCAM files are multi-extension FITS with a primary header and
        each detector stored in a subsequent extension.  VIRCAM uses
        ``INHERIT=T`` and each detector header will be merged with the
        primary header.
        Guide headers are not returned.
        Parameters
        ----------
        filename : `str`
            Path to a file in a format understood by this translator.
        primary : `dict`-like, optional
            The primary header obtained by the caller. This is sometimes
            already known, for example if a system is trying to bootstrap
            without already knowing what data is in the file. Will be
            merged with detector headers if supplied, else will be read
            from the file.
        Yields
        ------
        headers : iterator of `dict`-like
            Each detector header in turn. The supplied header will be merged
            with the contents of each detector header.
        Notes
        -----
        This translator class is specifically tailored to raw DECam data and
        is not designed to work with general FITS files. The normal paradigm
        is for the caller to have read the first header and then called
        `determine_translator()` on the result to work out which translator
        class to then call to obtain the real headers to be used for
        translation.
        """
        # Circular dependency so must defer import.
        from astro_metadata_translator.headers import merge_headers

        # Since we want to scan many HDUs we use astropy directly to keep
        # the file open rather than continually opening and closing it
        # as we go to each HDU.

        with fits.open(filename) as fits_file:
            # Astropy does not automatically handle the INHERIT=T in
            # DECam headers so the primary header must be merged.
            first_pass = True

            for hdu in fits_file:
                if first_pass:
                    if not primary:
                        primary = hdu.header
                    first_pass = False
                    continue

                header = hdu.header
                if "EXTNAME" not in header:  # Primary does not have
                    continue

                yield merge_headers([primary, header], mode="overwrite")

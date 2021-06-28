
__all__ = ("VircamTranslator", )

from astro_metadata_translator import cache_translation, FitsTranslator
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, Angle


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
    """
    _const_map = {"boresight_rotation_coord": "sky",
                  "detector_group": None,
                  "boresight_airmass": None,  # This could be calculated.
                  "boresight_rotation_angle": Angle(90 * u.deg),
                  "science_program": None,
                  "temperature": 300. * u.K,
                  "pressure": 985. * u.hPa,
                  "relative_humidity": None,
                  "altaz_begin": None,  # This could be calculated.
                  "location": None,
                  }

    """
    _trivial_map includes properties that can be taken directly from header
    """
    _trivial_map = {
        "exposure_id": "ESO DET EXP NO",
        "visit_id": "ESO DET EXP NO",
        "observation_id": "ESO DET EXP NO",
        "detector_exposure_id": "ESO DET EXP NO",
        "detector_num": "ESO DET CHIP NO",
        "detector_serial": "ESO DET CHIP NO",
        # "physical_filter": "HIERARCH ESO INS FILT1 NAME",
        "exposure_time": ("EXPTIME", dict(unit=u.s)),
        "dark_time": ("EXPTIME", dict(unit=u.s)),
        # This is a hack we need to merge to primary header
        "object": "ORIGIN",
        # "observation_type": "ESO DET CON OPMODE",
        "telescope": ("TELESCOP", dict(default="VISTA")),
        "instrument": ("INSTRUME", dict(default="VIRCAM")),
    }

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

        if "ORIGIN" in header:

            if header["ORIGIN"] == "ESO":

                return True
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
    def to_datetime_end(self):
        datetime_end = self.to_datetime_begin() + self.to_exposure_time()
        return datetime_end

    @cache_translation
    def to_tracking_radec(self):
        radec = SkyCoord(self._header["CRVAL1"], self._header["CRVAL2"],
                         frame="icrs", unit=(u.hourangle, u.deg))
        return radec

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
    def to_instrument(self):
        if self._header["INSTRUME"].strip(" ") == "VIRCAM":
            return "VIRCAM"
        else:
            # It should never get here, given can_translate().
            return "Unknown"

    def to_telescope(self):
        return self.to_instrument()

    @cache_translation
    def to_detector_name(self):
        return '{:02d}'.format(self._header["ESO DET CHIP NO"])

    @cache_translation
    def to_observation_type(self):
        return 'science'

    @classmethod
    def determine_translatable_headers(cls, filename, primary=None):
        """Given a file return all the headers usable for metadata translation.
        DECam files are multi-extension FITS with a primary header and
        each detector stored in a subsequent extension.  DECam uses
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
                if "HIERARCH ESO DET CHIP NO" not in header:  # Primary does not have
                    continue

                yield merge_headers([primary, header], mode="overwrite")

########################################################################3
## ObservationResults
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.static.models import stRxNames
from archive.scans.models import Scan, Offset
from archive.backends.models import Backend


class FocusResults(ClassTemplate):    
    """ There's one focus result for each backend used in the scan """
    backend = models.ForeignKey(Backend, null=True, blank=True,
                        help_text="Focus result related to this backend")
    focus = models.FloatField("Focus", null=True, blank=True, help_text="Unit=mm")
    focusError = models.FloatField("Focus Error", null=True, blank=True, help_text="Unit=mm")
    offset = models.FloatField("Offset", null=True, blank=True, help_text="Unit=mm")
    offsetError = models.FloatField("Offset Error", null=True, blank=True, help_text="Unit=mm")
    rmsResidual = models.FloatField("RMS Residual", null=True, blank=True, help_text="Unit=K")
    method = models.CharField("Method", blank=True, max_length=45)
    
    class Meta:
        db_table = 'FocusResults'
        verbose_name = 'Focus Result'
        verbose_name_plural = 'Focus Results'

    def __unicode__(self):
        return u'Focus results for %s' % (self.backend)


class PointingResults(ClassTemplate):
    """ There's two pointing result for each backend used in the scan, one for Az and one for El """
    backend = models.ForeignKey(Backend, null=True, blank=True,
                        help_text="Pointing result related to this backend")
    direction = models.CharField("Direction", blank=False, max_length=45)
    correction = models.FloatField("Correction", null=True, blank=True, help_text="Unit=arcsec")
    correctionError = models.FloatField("Correction Error", null=True, blank=True, help_text="Unit=arcsec")
    peak = models.FloatField("Peak", null=True, blank=True, help_text="Unit=K")
    peakError = models.FloatField("Peak Error", null=True, blank=True, help_text="Unit=K")
    integral = models.FloatField("Integral", null=True, blank=True, help_text="Unit=K.arcsec")
    integralError = models.FloatField("Integral Error", null=True, blank=True, help_text="Unit=K.arcsec")
    offset = models.FloatField("Offset", null=True, blank=True, help_text="Unit=mm")
    offsetError = models.FloatField("Offset Error", null=True, blank=True, help_text="Unit=mm")
    width = models.FloatField("Width", null=True, blank=True, help_text="Unit=arcsec")
    widthError = models.FloatField("Width Error", null=True, blank=True, help_text="Unit=arcsec")
    rmsResidual = models.FloatField("RMS Residual", null=True, blank=True, help_text="Unit=K")    
    method = models.CharField("Method", blank=True, max_length=45)
    
    class Meta:
        db_table = 'PointingResults'
        verbose_name = 'Pointing Result'
        verbose_name_plural = 'Pointing Results'

    def __unicode__(self):
        return u'Pointing results for %s' % (self.backend)


class CalibrationResults(ClassTemplate):
    """ There's one calibration result for each receiver in the scan. That's include each one of the HERA pixels """
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    receiver = models.ForeignKey(stRxNames, null=True, blank=True,
                    help_text="Calibrate the image-to-signal gain ratio for this receiver.")
                     
    frequencyImage = models.FloatField("Frequency Image", null=True, blank=True, help_text="Unit=GHz")
    xOffsetNasmyth = models.FloatField("x-Offset Nasmyth", null=True, blank=True, help_text="Unit=arcsec")
    yOffsetNasmyth = models.FloatField("y-Offset Nasmyth", null=True, blank=True, help_text="Unit=arcsec")
    lcalof = models.FloatField("Longitude Offset for Calibration sky counts", null=True, blank=True, help_text="Unit=arcsec")
    bcalof = models.FloatField("Latitude Offset for Calibration sky counts", null=True, blank=True, help_text="Unit=arcsec")
    h2omm = models.FloatField("Water Vapour Column", null=True, blank=True, help_text="Unit=mm")
    trx = models.FloatField("Receiver Temperature", null=True, blank=True, help_text="Unit=K")
    tsys = models.FloatField("System Temperature", null=True, blank=True, help_text="Unit=K")
    tcal = models.FloatField("Calibration Temperature", null=True, blank=True, help_text="Unit=K")
    tatms = models.FloatField("Atmospheric Emission Temperature (signal band)", null=True, blank=True, help_text="Unit=K")
    tatmi = models.FloatField("Atmoshperic Emission Temperature (image band)", null=True, blank=True, help_text="Unit=K")
    tauzen = models.FloatField("Atmospheric Zenith Opacity", null=True, blank=True, help_text="Unit=Neper")
    tauzenImage = models.FloatField("Atmospheric Zenith Opacity (image band)", null=True, blank=True, help_text="Unit=Neper")
    pcold = models.FloatField("Backend counts on Cold calibration load", null=True, blank=True, help_text="Unit=counts")
    phot = models.FloatField("Backend counts on Ambient calibration load", null=True, blank=True, help_text="Unit=counts")
    psky = models.FloatField("Backend counts on Sky", null=True, blank=True, help_text="Unit=counts")    
    
    class Meta:
        db_table = 'CalibrationResults'
        verbose_name = 'Calibration Result'
        verbose_name_plural = 'Calibration Results'

    def __unicode__(self):
        return u'Scan %s calibration results for %s' % (self.scan, self.receiver)


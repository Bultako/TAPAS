########################################################################3
## Receivers
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.static.models import stRxNames
from archive.scans.models import Project, Scan


class PredefinedReceiver(ClassTemplate):
    project = models.ForeignKey(Project, verbose_name="Project")
    rxName = models.ForeignKey(stRxNames, verbose_name="Receiver")
    receiverComment = models.TextField("Comment", blank=True)
    class Meta:
        db_table = 'PredefinedReceivers'
        verbose_name = 'Predefined Receiver'
        verbose_name_plural = 'Predefined Receivers'

    def __unicode__(self):
        return u'%s' % (self.rxName)


class Receiver(ClassTemplate):
    rxName = models.ForeignKey(stRxNames, verbose_name="Receiver")
    scan = models.ForeignKey(Scan, verbose_name="Scan")
    class Meta:
        db_table = 'Receivers'

    def __unicode__(self):
        return u'%s in scan %s' % (self.rxName, self.scan)


class RxReceiverCfg(ClassTemplate):
    receiver = models.ForeignKey(Receiver, verbose_name="Receiver")
    lineName = models.CharField("Line name", blank=True, max_length=45)
    frequency = models.FloatField("Frequency", null=True, blank=True, help_text="Unit=GHz")
    SIDEBAND_CHOICES = (
        ('LSB', 'LSB (Low Side Band)'),
        ('USB', 'USB ()'), ) # ??
    
    sideBand = models.CharField("Sideband", blank=True, max_length=20, choices=SIDEBAND_CHOICES)
    
    DOPPLER_CHOICES = (
        ('DOPPLER', 'Doppler'),
        ('FIXED', 'Fixed'), )
    doppler = models.CharField("Doppler Correction", blank=True, max_length=20, choices=DOPPLER_CHOICES)
    
    WIDTH_CHOICES = (
        ('WIDE', 'Wide'),
        ('NARROW', 'Narrow'), )
    width = models.CharField("Width", blank=True, max_length=20, choices=WIDTH_CHOICES)
    gainImage = models.FloatField("Gain Image", null=True, blank=True, help_text="Unit=--")
    tempCold = models.FloatField("Cold Temperature", null=True, blank=True, help_text="Unit=K")
    tempAmbient = models.FloatField("Ambient Temperature", null=True, blank=True, help_text="Unit=K")
    effForward = models.FloatField("Forward Efficiency", null=True, blank=True, help_text="Unit=--")
    effBeam = models.FloatField("Beam Efficiency", null=True, blank=True, help_text="Unit=--")
    scale = models.CharField("Scale", blank=True, max_length=20)
    iPixel = models.IntegerField("Selected Pixel", null=True, blank=True, help_text="Unit=--")
    nPixels = models.IntegerField("# of Pixels", null=True, blank=True, help_text="Unit=--")
    centerIF = models.FloatField("Center IF", null=True, blank=True, help_text="Unit=GHz")
    bandwidth = models.FloatField("Bandwidth", null=True, blank=True, help_text="Unit=GHz")
    distributionBoxInput = models.IntegerField("Distribution-Box Input", null=True, blank=True, help_text="Unit=--")
    IF2 = models.FloatField("IF2", null=True, blank=True, help_text="Unit=GHz")
    isFlippingIF2 = models.BooleanField("Is flipping IF2", null=True, blank=True)
    polarization = models.CharField("Polarization", blank=True, max_length=20)
    useSpecialLO = models.BooleanField("Use special LO", null=True, blank=True)
    derotatorAngle = models.FloatField("Derotator Angle", null=True, blank=True, help_text="For HERA. Unit=rad")
    
    DEROTATORSYSTEM_CHOICES = (
        ('NASMYTH', 'Nasmyth'),
        ('HORIZON', 'Horizon'),
        ('EQUATORIAL', 'Equatorial'),
        ('FRAME', 'Frame (same as Nasmyth)'),
        ('SKY', 'Sky (same as Equatorial)'),)
    derotatorSystem = models.CharField("Derotator System", blank=True, max_length=20, 
                    choices=DEROTATORSYSTEM_CHOICES, help_text="For HERA")
    
    class Meta:
        db_table = 'RxReceiversCfg'
        verbose_name = 'Het/HERA Configuration'
        verbose_name_plural = 'Het/HERA Configurations'

    def __unicode__(self):
        return u'Linename "%s" at freq. %f' % (self.lineName, self.frequency)


class RxBolometerCfg(ClassTemplate):
    receiver = models.ForeignKey(Receiver, verbose_name="Receiver")
    nChannels = models.IntegerField("Number of channels", null=True, blank=True, help_text="Unit=--")
    channel = models.IntegerField("Choosen channel", null=True, blank=True, help_text="Unit=--")
    gainBolometer = models.FloatField("Gain bolometer", null=True, blank=True, help_text="Unit=--")
    class Meta:
        db_table = 'RxBolometerCfg'
        verbose_name = 'Bolometer Configuration'
        verbose_name_plural = 'Bolometer Configurations'

    def __unicode__(self):
        return u'%s' % (self.receiver) # ...TBD


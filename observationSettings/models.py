########################################################################3
## ObservationSettings
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.static.models import stRxNames
from archive.scans.models import Scan, Offset
from archive.static.models import stSystemNames

class TipSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    tipFrom = models.FloatField("Airmass Start", null=True, blank=True, help_text="Unit=--")
    tipTo = models.FloatField("Airmass End", null=True, blank=True, help_text="Unit=--")
    tipBy = models.FloatField("Airmass step", null=True, blank=True, help_text="Unit=--")
    doSlew = models.BooleanField("Do Slew", null=True, blank=True)
    class Meta:
        db_table = 'TipSettings'
        verbose_name = 'Tip Setting'
        verbose_name_plural = 'Tip Settings'

    def __unicode__(self):
        return u'Scan %s tip settings' % (self.scan)

    class Admin:
        pass


class FocusSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    len = models.FloatField("Length", null=True, blank=True, help_text="Unit=mm")
    class Meta:
        db_table = 'FocusSettings'
        verbose_name = 'Focus Setting'
        verbose_name_plural = 'Focus Settings'

    def __unicode__(self):
        return u'Scan %s focus settings' % (self.scan)

    class Admin:
        pass


class PointingSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    len = models.FloatField("Length", null=True, blank=True, help_text="Unit=rad")
    doDoubleBeam = models.BooleanField("Do double-beam pointing", null=True, blank=True)
    nOtf = models.IntegerField("Number of OTF", null=True, blank=True)
    tOtf = models.FloatField("Time per OTF", null=True, blank=True, help_text="Unit=s")
    class Meta:
        db_table = 'PointingSettings'
        verbose_name = 'Pointing Setting'
        verbose_name_plural = 'Pointing Settings'

    def __unicode__(self):
        return u'Scan %s pointing settings' % (self.scan)

    class Admin:
        pass


class OTFMapSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    xStart = models.FloatField("x-Offset of start", null=True, blank=True,
            help_text="Unit=rad")
    yStart = models.FloatField("y-Offset of start", null=True, blank=True,
            help_text="Unit=rad")
    xEnd = models.FloatField("x-Offset of end", null=True, blank=True,
            help_text="Unit=rad")
    yEnd = models.FloatField("y-Offset of end", null=True, blank=True,
            help_text="Unit=rad")
    
    system = models.ForeignKey(stSystemNames, verbose_name="system of reference")
    doReference = models.BooleanField("Do reference", null=True, blank=True)
    reference = models.ForeignKey(Offset, null=True, blank=True, #edit_inline=True, see why it fails!
            help_text="Off-source reference position")
    
    croLoop = models.CharField(blank=True, max_length=255,
            help_text="Sequence of \"R\" (off-source Reference) or \"O\" (on-source OTF). E.g. \"ROOR\"")
    xStep = models.FloatField("x-Step", null=True, blank=True, help_text="Unit=rad")
    yStep = models.FloatField("y-Step",null=True, blank=True, help_text="Unit=rad")
    alternativeSpeedTotf = models.CharField(blank=True, max_length=45) # ??
    speedStart = models.FloatField("Speed at start", null=True, blank=True, help_text="Unit=rad/s")
    speedEnd = models.FloatField("Speed at end", null=True, blank=True, help_text="Unit=rad/s")
    timePerOtf = models.FloatField("Time per OTF", null=True, blank=True, help_text="Unit=s")
    timePerReference = models.FloatField("Time per off-source reference", null=True, blank=True, help_text="Unit=s")
    doZigzag = models.BooleanField("Do zig-zag", null=True, blank=True)
    class Meta:
        db_table = 'OTFMapSettings'
        verbose_name = 'OTFMap Setting'
        verbose_name_plural = 'OTFMap Settings'

    def __unicode__(self):
        return u'Scan %s OTFmap settings' % (self.scan)

    class Admin:
        pass


class OnOffSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    xOffset = models.FloatField("x-Offset of \"on-source\" position", null=True, blank=True)
    yOffset = models.FloatField("y-Offset of \"on-source\" position", null=True, blank=True)
    system = models.ForeignKey(stSystemNames, verbose_name="system of reference")
    reference = models.ForeignKey(Offset, null=True, blank=True, help_text="Off-source reference position")
    doSymmetric = models.BooleanField("Do symmetric", null=True, blank=True)
    doSwWobbler = models.BooleanField("Do wobbler switching", null=True, blank=True)
    class Meta:
        db_table = 'OnOffSettings'
        verbose_name = 'OnOff Setting'
        verbose_name_plural = 'OnOff Settings'

    def __unicode__(self):
        return u'Scan %s OnOff settings' % (self.scan)

    class Admin:
        pass


class CalibrationSettings(ClassTemplate):
    scan = models.ForeignKey(Scan, help_text="Information related to this scan")
    doAmbient = models.BooleanField("Do ambient subscan", null=True, blank=True)
    doCold = models.BooleanField("Do cold subscan", null=True, blank=True)
    doSky = models.BooleanField("Do sky subscan", null=True, blank=True)
    skyOffset = models.ForeignKey(Offset, null=True, blank=True, verbose_name="Sky Offset")
    gainImageRx = models.ForeignKey(stRxNames, null=True, blank=True,
                    db_column='gainimagerx', help_text="Calibrate the image-to-signal gain ratio for this receiver.")
    doGrid = models.BooleanField("Do grid", null=True, blank=True)
    class Meta:
        db_table = 'CalibrationSettings'
        verbose_name = 'Calibration Setting'
        verbose_name_plural = 'Calibration Settings'

    def __unicode__(self):
        return u'Scan %s calibration settings' % (self.scan)

    class Admin:
        pass


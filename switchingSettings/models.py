########################################################################3
## SwitchingSettings
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.static.models import stSwitchingModes
from archive.scans.models import Scan
from archive.receivers.models import Receiver

class SwitchingCfg(ClassTemplate):
    mode = models.ForeignKey(stSwitchingModes, verbose_name="Switching Mode")
    scan = models.ForeignKey(Scan)
    nCycles = models.IntegerField("Number of Cycles", null=True, blank=True)
    nPhases = models.IntegerField("Number of Phases", null=True, blank=True)
    timePerPhase = models.FloatField("Time per Phase", null=True, blank=True, help_text="Unit=s")
    timePerRecord = models.FloatField("Time per Second", null=True, blank=True, help_text="Unit=s")
    wobblerThrow = models.FloatField("Wobbler Throw", null=True, blank=True, help_text="Unit=rad")
    class Meta:
        db_table = 'SwitchingValues'
        verbose_name = 'Switching Config'
        verbose_name_plural = 'Switching Configs'

    def __unicode__(self):
        return u'Scan %s: switching %s' % (self.scan, self.mode) 

class FrequencySwitching(ClassTemplate):
    receiver = models.ForeignKey(Receiver)
    switchingCfg = models.ForeignKey(SwitchingCfg)
    frequencyThrow = models.FloatField("Frequency Throw", null=True, blank=True, help_text="Unit=GHz")
    frequencyOffset1 = models.FloatField("Frequency Offset #1", null=True, blank=True, help_text="Unit=GHz")
    frequencyOffset2 = models.FloatField("Frequency Offset #2", null=True, blank=True, help_text="Unit=GHz")
    class Meta:
        db_table = 'FrequencySwitching'
        verbose_name = 'Frequency Switching'
        verbose_name_plural = 'Frequency Switchings'

    def __unicode__(self):
        return u'%f' % (self.frequencyThrow)


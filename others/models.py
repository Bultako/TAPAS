########################################################################3
## AUX
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.static.models import stTelescopeStates
from archive.scans.models import Project


########################################################################3
## Weather
########################################################################3

class WeatherStation(ClassTemplate):
    timeStamp = models.DateTimeField("Time Stamp", unique=True)
    electricalField = models.FloatField("Electrical Field", null=True, blank=True)
    windVel = models.FloatField("Wind velocity", null=True, blank=True)
    windVelMax = models.FloatField("Maximum wind velocity", null=True, blank=True)
    windDir = models.FloatField("Wind direction", null=True, blank=True)
    humidity = models.FloatField("Humidity", null=True, blank=True)
    pressure = models.FloatField("Pressure", null=True, blank=True)
    temperature = models.FloatField("Temperature", null=True, blank=True)
    class Meta:
        db_table = 'WeatherStation'
        verbose_name = 'Weather Station Info'
        verbose_name_plural = 'Weather Station Info'

    def __unicode__(self):
        return u'Weather Station Info at %s' % (self.timeStamp)


class WeatherTau(ClassTemplate):
    timeStamp = models.DateTimeField("Time Stamp", null=True, blank=True, unique=True)
    tau = models.FloatField("Tau", null=True, blank=True)
    sigma = models.FloatField("Sigma", null=True, blank=True)
    fit = models.FloatField("Fit", null=True, blank=True)
    class Meta:
        db_table = 'WeatherTau'
        verbose_name = 'Weather Tau Info'
        verbose_name_plural = 'Weather Tau Info'

    def __unicode__(self):
        return u'Weather Tau Info at %s' % (self.timeStamp)


########################################################################3
## Telescope Status
########################################################################3

class TelescopeStatus(ClassTemplate):
    telescopeState = models.ForeignKey(stTelescopeStates, verbose_name="Telescope State")
    timeStamp = models.DateTimeField("Time Stamp", null=True, blank=True, unique=True)
    class Meta:
        db_table = 'TelescopeStatus'
        verbose_name = 'Telescope Status'
        verbose_name_plural = 'Telescope Status'

    def __unicode__(self):
        return u'Telescope: %s at %s' % (self.telescopeState, self.timeStamp)


########################################################################3
## Pools
########################################################################3

class Pool(ClassTemplate):
    name = models.CharField("Name", max_length=255)
    description = models.CharField("Description", blank=True, max_length=255)
    projects = models.ManyToManyField(Project, db_table = "Pools_has_Projects") # Automatically generated!
    class Meta:
        db_table = 'Pools'
        verbose_name = 'Pool'
        verbose_name_plural = 'Pools'

    def __unicode__(self):
        return u'%s' % (self.name)

class PoolPeriod(ClassTemplate):
    pool = models.ForeignKey(Pool, verbose_name="Pool")
    startDate = models.DateTimeField("Start Date")
    endDate = models.DateTimeField("End Date")
    class Meta:
        db_table = 'PoolPeriods'
        verbose_name = 'Pool Period'
        verbose_name_plural = 'Pool Periods'

    def __unicode__(self):
        return u'%s (%s - %s)' % (self.pool.name, self.startDate, self.endDate)


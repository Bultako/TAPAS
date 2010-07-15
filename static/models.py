########################################################################3
## Static
########################################################################3
from django.db import models
from datetime import datetime
from archive.datafiller.models import ClassTemplate

class stPredefinedComments(models.Model):
    comment_text = models.TextField("Comment", blank=True)
    technical = models.BooleanField(null=True, blank=True)
    class Meta:
        db_table = 'stPredefinedComments'
        verbose_name = 'Predefined Comment'
        verbose_name_plural = 'Predefined Comments'

    def __unicode__(self):
        return u'%s' % (self.rxName)

# UNITS ??
class stPointingModels(ClassTemplate):
    timeStamp = models.DateTimeField("Time Stamp", null=True, blank=True, unique=True, default=datetime.now)
    p1 = models.FloatField(null=True, blank=True)
    p2 = models.FloatField(null=True, blank=True)
    p3 = models.FloatField(null=True, blank=True)
    p4 = models.FloatField(null=True, blank=True)
    p5 = models.FloatField(null=True, blank=True)
    p7 = models.FloatField(null=True, blank=True)
    p8 = models.FloatField(null=True, blank=True)
    p9 = models.FloatField(null=True, blank=True)
    rxho = models.FloatField("rxHorizontal", null=True, blank=True)
    rxve = models.FloatField("rxVertical", null=True, blank=True)
    refract3 = models.FloatField("refract3", null=True, blank=True)
    subref_rotationzero = models.FloatField("subref_rotationzero", null=True, blank=True)
    subref_rotationphi0 = models.FloatField("subref_rotationphi0", null=True, blank=True)
    subref_rotationradius = models.FloatField("subref_rotationradius", null=True, blank=True)
    encoder_sincol = models.FloatField("encoder_sincol", null=True, blank=True)
    encoder_coscol = models.FloatField("encoder_coscol", null=True, blank=True)
    class Meta:
        db_table = 'stPointingModels'
        verbose_name = 'Poiting Model'
        verbose_name_plural = 'Pointing Models'

    def __unicode__(self):
        return u'%s' % (self.timeStamp)

class stRxNames(models.Model):
    name = models.CharField(blank=True, max_length=20)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stRxNames'
        verbose_name = 'Receiver name'
        verbose_name_plural = 'Receiver names'

    def __unicode__(self):
        return u'%s' % (self.name)
    
    @staticmethod
    def get(name):
        if (name.lower() == 'bolometer'): 
            name = "MAMBO2"
        elif (name.upper().find('HERA1') != -1): #because of HERA pixels separation in DM
            name = 'HERA1 Pixel 1'
        elif (name.upper().find('HERA2') != -1): #because of HERA pixels separation in DM
            name = 'HERA2 Pixel 1'
                
        return stRxNames.objects.get(name = name)

class stProjectModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.CharField(blank=True, max_length=255)
    class Meta:
        db_table = 'stProjectModes'
        verbose_name = 'Project Mode'
        verbose_name_plural = 'Project Modes'

    def __unicode__(self):
        return u'%s' % (self.name)

class stBkNames(models.Model):
    name = models.CharField(blank=True, max_length=20)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stBkNames'
        verbose_name = 'Backend name'
        verbose_name_plural = 'Backend names'

    def __unicode__(self):
        return u'%s' % (self.name)

class stObservingModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stObservingModes'
        verbose_name = 'Observing Mode'
        verbose_name_plural = 'Observing Modes'

    def __unicode__(self):
        return u'%s' % (self.name)

class stFileLocations(models.Model):
    locationname = models.CharField(blank=True, max_length=45)
    hostname = models.CharField(blank=True, max_length=45)
    path = models.CharField(blank=True, max_length=255)
    class Meta:
        db_table = 'stFileLocations'
        verbose_name = 'File Location'
        verbose_name_plural = 'File Locations'

    def __unicode__(self):
        return u'%s' % (self.locationname)

class stSoftwareVersions(models.Model):
    software = models.CharField(max_length=45)
    version = models.CharField(max_length=45)
    date = models.DateTimeField(null=True, blank=True, default=datetime.now)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSoftwareVersions'
        verbose_name = 'Software Version'
        verbose_name_plural = 'Software Versions'

    def __unicode__(self):
        return u'%s %s (%s)' % (self.software, self.version, self.date)

class stTelescopeStates(models.Model):
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stTelescopeStates'
        verbose_name = 'Telescope State'
        verbose_name_plural = 'Telescope States'

    def __unicode__(self):
        return u'%s' % (self.name)

class stSwitchingModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSwitchingModes'
        verbose_name = 'Switching Mode'
        verbose_name_plural = 'Switching Modes'

    def __unicode__(self):
        return u'%s' % (self.name)

class stSystemNames(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSystemNames'
        verbose_name = 'System Name'
        verbose_name_plural = 'System Names'

    def __unicode__(self):
        return u'%s' % (self.name)

class SourceSearch_Receivers(models.Model):

    field_label = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


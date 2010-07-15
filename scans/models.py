########################################################################3
## Scans
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from django.contrib.auth.models import User
from archive.static.models import stSystemNames, stObservingModes, stPointingModels, \
                                stPredefinedComments, stProjectModes, stSoftwareVersions


class Offset(ClassTemplate):
    system = models.ForeignKey(stSystemNames, verbose_name="system of reference")
    xOffset = models.FloatField("x-Offset", null=True, blank=True, help_text="Unit=rad")
    yOffset = models.FloatField("y-Offset", null=True, blank=True, help_text="Unit=rad")
    class Meta:
        db_table = 'Offsets'

    def __unicode__(self):
        return u'(%f, %f) in system %s' % (self.xOffset, self.yOffset, self.system)


class Project(ClassTemplate):
    pi = models.ForeignKey(User, verbose_name="Principal Investigator", related_name="pi")
    projectId = models.CharField("Project ID", blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)
    
    # PRIORITY_CHOICES ??
    priority = models.IntegerField(null=True, blank=True) #a.k.a. HERA projectStatus
    
    # RANKING_CHOICES ??
    ranking = models.IntegerField(null=True, blank=True) #a.k.a. HERA grade
    allocatedTime = models.FloatField("Allocated Time", null=True, blank=True, 
                help_text="Unit=hours")
    usedTime = models.FloatField("Used Time", null=True, blank=True, help_text="Unit=hours")
    requiredOpacity = models.FloatField("Required Opacity", null=True, blank=True)
    requiredWaterVapor = models.FloatField("Required Water vapor", null=True, blank=True, help_text="Unit=mm")
    requiredSkynoise = models.CharField("Required Skynoise", blank=True, max_length=18)
    weatherComment = models.TextField("Weather Comment", blank=True)
    projectModes = models.ManyToManyField(stProjectModes, 
                    db_table = "Projects_has_stProjectModes",
                    verbose_name="Project Modes",
                    help_text="Modes planned to be used in the project") # Automatically generated!
    projectComment = models.TextField("Project Comment", blank=True)
    projectBriefComment = models.TextField("Project Brief Comment", blank=True)
    projectRemarkComment = models.TextField("Project Remark Comment", blank=True, help_text="For admin")
    is_LKP = models.BooleanField("Large Key Programme", null=True, blank=True)

    class Meta:
        db_table = 'Projects'

    def __unicode__(self):
        return u'%s (%s)' % (self.projectId, self.pi)

class Scan(ClassTemplate):
    #From the observingMode specs in PaKo XML
    observer = models.ForeignKey(User, verbose_name="Observer", related_name="observer")
    
    observingMode = models.ForeignKey(stObservingModes, verbose_name="Observing Mode")
    pointingModel = models.ForeignKey(stPointingModels, verbose_name="Pointing Model")
    project = models.ForeignKey(Project)
    
    #treated like a primary key!
    ncsId = models.CharField("NCS Scan ID", blank=True, max_length=255, unique=True, null=False) 
    
    startTime = models.DateTimeField("Start time", null=True, blank=True)
    endTime = models.DateTimeField("End time", null=True, blank=True)
    LST = models.FloatField(null=True, blank=True, help_text="Local Sidereal Time ")
    MJD = models.FloatField(null=True, blank=True, help_text="Modified Julian Date")
    tau = models.FloatField("Tau", null=True, blank=True)
    nSubscans = models.IntegerField("# of subscans", null=True, blank=True)
    tSubscans = models.FloatField("Subscan time", null=True, blank=True, help_text="Unit=s")
    softwareVersions = models.ManyToManyField(stSoftwareVersions, verbose_name="Software versions",
                        db_table = "stSoftwareVersions_usedin_Scans",
                        help_text="Software versions used during this scan") # Automatically generated!
    offsets = models.ManyToManyField(Offset,
                db_table = "Scans_has_Offsets") # Automatically generated!
    class Meta:
        db_table = 'Scans'
        
    def __unicode__(self):
        return u'%s (bdId=%s)' % (self.ncsId, self.id)

    def settings(self):
        """ Return the appropiate class of ObservingSettings of the Scan: Tip, pointing, focus... 
        """
        pass
    
    def results(self):
        """ Return the appropiate class of ObservingResults of the Scan: calibration, pointing or focus
        """
        pass

#possibly erase in the future!
#class Subscan(models.Model):
    #scan = models.ForeignKey(Scan)
    #timePerSubscan = models.FloatField("Subscan time", null=True, blank=True)
    #class Meta:
        #db_table = 'Subscans'

    #def __unicode__(self):
        #pass
        ##return u'%s' % (self.rxName)

    #class Admin:
        #pass

#not clear yet if it's going to be used this class or
#a comment extension for Django!
class ScanComment(ClassTemplate):
    scan = models.ForeignKey(Scan)
    predefinedComment = models.ForeignKey(stPredefinedComments, verbose_name="Predefined Comment")
    User = models.ForeignKey(User)
    extraComment = models.TextField("Extra comment", blank=True)
    class Meta:
        db_table = 'ScanComments'
        verbose_name = 'Scan comment'
        verbose_name_plural = 'Scan comments'

    def __unicode__(self):
        return u'Comment by user %s in scan %s' % (self.User, self.scan)


########################################################################3
## Sources
########################################################################3

from django.db import models
from archive.datafiller.models import ClassTemplate

from archive.scans.models import Project, Scan

class SourceRadialVelocity(ClassTemplate):
    REFERENCEFRAME_CHOICES = (
        ('LSR', 'LSR'),
        ('', 'none'),
        ('3K', '3K'),
        ('galactocentric', 'galactocentric'),
        ('body', 'body'),
        ('barycentric', 'barycentric'),
        ('heliocentric', 'heliocentric'),
        ('geocentric', 'geocentric'),
        ('topocentric', 'topocentric'),
        
    )
    referenceFrame = models.CharField("Reference system", max_length=45, 
            choices=REFERENCEFRAME_CHOICES)
    convention = models.CharField(max_length=45)
    velocity = models.FloatField(null=True, blank=True, help_text="Unit=m/s")
    xOffsetDoppler = models.FloatField("x-Offset Doppler", null=True, blank=True, help_text="Unit=rad")
    yOffsetDoppler = models.FloatField("y-Offset Doppler", null=True, blank=True, help_text="Unit=rad")
    class Meta:
        db_table = 'SourceRadialVelocities'
        verbose_name = 'Source Radial Velocity'
        verbose_name_plural = 'Source Radial Velocities'

    def __unicode__(self):
        return u'%f' % (self.velocity)


class PredefinedSource(ClassTemplate):
    project = models.ForeignKey(Project)
    sourceRadialVelocity = models.ForeignKey(SourceRadialVelocity, 
                    verbose_name="Source radial velocity")
    sourceName = models.CharField("Source name", max_length=255)
    BASISSYSTEM_CHOICES= (
     ('Equatorial','equatorial'),
     ('Horizontal','horizontal'),
     ('Galactic','galactic'),
     ('apparentEquatorial','apparentEquatorial'),
     ('apparentEcliptic','apparentEcliptic'),
     ('Ecliptic','ecliptic'),
     ('haDec','haDec'),)

    basisSystem = models.CharField("Basis system", blank=True, max_length=45, choices=BASISSYSTEM_CHOICES)
    
    equinoxSystem = models.CharField("Equinox system", blank=True, max_length=20)
    equinoxYear = models.FloatField("Equinox year", null=True, blank=True, help_text="Unit=year")
    
    # Field renamed because it was a Python reserved word.
    lambdaField = models.FloatField("Lambda", db_column='lambda', null=True, blank=True, 
                help_text="Unit=rad (RA)")
    beta = models.FloatField("Beta", null=True, blank=True, help_text="Unit=rad (Decl)")
    priority = models.FloatField("Priority", null=True, blank=True)
    aimedRMS = models.FloatField("Aimed RMS", null=True, blank=True, help_text="Unit=mJy")
    actualRMS = models.FloatField("Actual RMS", null=True, blank=True, help_text="Unit=mJy")
    resolution = models.FloatField("Resolution", null=True, blank=True, help_text="Unit=Km/s")
    flux = models.FloatField("Flux", null=True, blank=True, help_text="Unit=mJy")
    sourceComment = models.TextField("Comment", blank=True, null=True)
    class Meta:
        db_table = 'PredefinedSources'
        verbose_name = 'Predefined Source'
        verbose_name_plural = 'Predefined Sources'

    def __unicode__(self):
        return u'%s' % (self.sourceName)


class ObservedSource(ClassTemplate):
    sourceRadialVelocity = models.ForeignKey(SourceRadialVelocity,
                    verbose_name="Source radial velocity")
    scan = models.ForeignKey(Scan)
    sourceName = models.CharField("Source name", max_length=255)
    
    BASISSYSTEM_CHOICES= (
     ('Equatorial','equatorial'),
     ('Horizontal','horizontal'),
     ('Galactic','galactic'),
     ('apparentEquatorial','apparentEquatorial'),
     ('apparentEcliptic','apparentEcliptic'),
     ('Ecliptic','ecliptic'),
     ('haDec','haDec'),
    )
    
    basisSystem = models.CharField("Basis system", blank=True, max_length=45, choices=BASISSYSTEM_CHOICES)
    
    equinoxSystem = models.CharField("Equinox system", blank=True, max_length=20)
    equinoxYear = models.FloatField("Equinos year", null=True, blank=True, help_text="Unit=year")
    
    # Field renamed because it was a Python reserved word.
    lambdaField = models.FloatField("Lambda", db_column='lambda', null=True, blank=True,
                    help_text="Unit=rad (RA)")
    beta = models.FloatField("Beta", null=True, blank=True, help_text="Unit=rad (Decl)")
    
    descriptiveSystem = models.CharField("Descriptive system", blank=True, max_length=45)
    alphaD = models.FloatField("alphaD", null=True, blank=True, help_text="Unit=rad")
    betaD = models.FloatField("betaD", null=True, blank=True, help_text="Unit=rad")
    gammaD = models.FloatField("gammaD", null=True, blank=True, help_text="Unit=rad")
    projection = models.CharField("projection", blank=True, max_length=45)
    lambdaProjection = models.FloatField("lambda Projection", null=True, blank=True, help_text="Unit=rad")
    betaProjection = models.FloatField("beta Projection", null=True, blank=True, help_text="Unit=rad")
    kappaProjection = models.FloatField("kappa Projection", null=True, blank=True, help_text="Unit=rad")
    #topology.azimuthWrap in PaKo
    topology = models.CharField("Topology", blank=True, max_length=20)
    sourceComment = models.TextField("Comment", blank=True, null=True)
    class Meta:
        db_table = 'ObservedSources'
        verbose_name = 'Observed source'
        verbose_name_plural = 'Observed sources'

    def __unicode__(self):
        return u'%s' % (self.sourceName)


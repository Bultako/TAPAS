# This is an auto-generated customized Django model module for the IRAM-30m Archive
# If you provide an SQL script, the models' order should be OK
# In other case, please rearrange models' order!
#
# Also Many to Many tables ('*_has_*' or '*_usedin_*') are ignored and replaced with ManyToManyField. Please check it!
#
# You'll have to do the following manually to clean this up:
#     * Replace any reference to model User to use django.user :%s/DjangoUsers/User/g
#     * Fix CharField max_length: 60->20 ; 135 -> 45 ; 765 -> 255
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.


########################################################################3
## Static
########################################################################3
from django.db import models

class stPredefinedComments(models.Model):
    comment_text = models.TextField(blank=True)
    technical = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'stPredefinedComments'

class stPointingModels(models.Model):
    p1 = models.FloatField(null=True, blank=True)
    p2 = models.FloatField(null=True, blank=True)
    p3 = models.FloatField(null=True, blank=True)
    p4 = models.FloatField(null=True, blank=True)
    p5 = models.FloatField(null=True, blank=True)
    p7 = models.FloatField(null=True, blank=True)
    p8 = models.FloatField(null=True, blank=True)
    p9 = models.FloatField(null=True, blank=True)
    rxho = models.FloatField(null=True, blank=True)
    rxve = models.FloatField(null=True, blank=True)
    refract3 = models.FloatField(null=True, blank=True)
    subref_rotationzero = models.FloatField(null=True, blank=True)
    subref_rotationphi0 = models.FloatField(null=True, blank=True)
    subref_rotationradius = models.FloatField(null=True, blank=True)
    encoder_sincol = models.FloatField(null=True, blank=True)
    encoder_coscol = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'stPointingModels'

class stRxNames(models.Model):
    name = models.CharField(blank=True, max_length=20)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stRxNames'

class stProjectModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.CharField(blank=True, max_length=255)
    class Meta:
        db_table = 'stProjectModes'

class stBkNames(models.Model):
    name = models.CharField(blank=True, max_length=20)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stBkNames'

class stObservingModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stObservingModes'

class stFileLocations(models.Model):
    locationname = models.CharField(blank=True, max_length=45)
    hostname = models.CharField(blank=True, max_length=45)
    path = models.CharField(blank=True, max_length=255)
    class Meta:
        db_table = 'stFileLocations'

class stSoftwareVersions(models.Model):
    software = models.CharField(unique=True, max_length=45)
    version = models.CharField(unique=True, max_length=20)
    date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSoftwareVersions'

class stTelescopeStates(models.Model):
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stTelescopeStates'

class stSwitchingModes(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSwitchingModes'

class stSystemNames(models.Model):
    name = models.CharField(blank=True, max_length=45)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'stSystemNames'



########################################################################3
## Users
########################################################################3

from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
    #username = models.CharField(max_length=90)
    #first_name = models.CharField(blank=True, max_length=90)
    #last_name = models.CharField(blank=True, max_length=90)
    #email = models.CharField(blank=True, max_length=45)
    #passwd = models.CharField(blank=True, max_length=255)
    #is_staff = models.IntegerField(null=True, blank=True)
    #is_active = models.IntegerField(null=True, blank=True)
    #is_superuser = models.IntegerField(null=True, blank=True)
    #last_login = models.DateTimeField(null=True, blank=True)
    #date_joined = models.DateTimeField(null=True, blank=True)
    #class Meta:
        #db_table = 'User'

class UsersProfiles(models.Model):
    user = models.ForeignKey(User)
    institute = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=180)
    class Meta:
        db_table = 'UsersProfiles'



########################################################################3
## Scans
########################################################################3

from django.db import models
from django.contrib.auth.models import User

class Offsets(models.Model):
    system = models.ForeignKey(stSystemNames)
    xoffset = models.FloatField(null=True, blank=True)
    yoffset = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'Offsets'

class Projects(models.Model):
    observer = models.ForeignKey(User)
    pi = models.ForeignKey(User)
    projectid = models.IntegerField(null=True, blank=True)
    title = models.CharField(blank=True, max_length=255)
    priority = models.IntegerField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)
    allocatedtime = models.FloatField(null=True, blank=True)
    usedtime = models.FloatField(null=True, blank=True)
    projectcomment = models.TextField(blank=True)
    requiredopacity = models.FloatField(null=True, blank=True)
    requiredskynoise = models.CharField(blank=True, max_length=18)
    weathercomment = models.TextField(blank=True)
    stprojectmodes = models.ManyToManyField(db_table = "Projects_has_stProjectModes") # Automatically generated!
    class Meta:
        db_table = 'Projects'

class Scans(models.Model):
    system = models.ForeignKey(stSystemNames, null=True, blank=True)
    stobservingmodes = models.ForeignKey(stObservingModes)
    stpointingmodels = models.ForeignKey(stPointingModels)
    projects = models.ForeignKey(Projects)
    ncsid = models.IntegerField(null=True, blank=True)
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    lst = models.FloatField(null=True, blank=True)
    mjd = models.FloatField(null=True, blank=True)
    nsubscans = models.IntegerField(null=True, blank=True)
    tsubscans = models.FloatField(null=True, blank=True)
    stsoftwareversions = models.ManyToManyField(db_table = "stSoftwareVersions_usedin_Scans") # Automatically generated!
    offsets = models.ManyToManyField(db_table = "Scans_has_Offsets") # Automatically generated!
    class Meta:
        db_table = 'Scans'

class Subscans(models.Model):
    scans = models.ForeignKey(Scans)
    timepersubscan = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'Subscans'

class ScanComments(models.Model):
    scans = models.ForeignKey(Scans)
    stpredefinedcomments = models.ForeignKey(stPredefinedComments)
    User = models.ForeignKey(User)
    extra_comment = models.TextField(blank=True)
    class Meta:
        db_table = 'ScanComments'



########################################################################3
## Receivers
########################################################################3

from django.db import models

class PredefinedReceivers(models.Model):
    projects = models.ForeignKey(Projects)
    strxnames = models.ForeignKey(stRxNames)
    commentsreceiver = models.TextField(blank=True)
    class Meta:
        db_table = 'PredefinedReceivers'

class Receivers(models.Model):
    strxnames = models.ForeignKey(stRxNames)
    scans = models.ForeignKey(Scans)
    class Meta:
        db_table = 'Receivers'

class RxReceiversCfg(models.Model):
    receivers = models.ForeignKey(Receivers)
    linename = models.CharField(blank=True, max_length=45)
    frequency = models.FloatField(null=True, blank=True)
    sideband = models.CharField(blank=True, max_length=20)
    doppler = models.CharField(blank=True, max_length=20)
    width = models.CharField(blank=True, max_length=20)
    gainimage = models.FloatField(null=True, blank=True)
    tempcold = models.FloatField(null=True, blank=True)
    tempambient = models.FloatField(null=True, blank=True)
    effforward = models.FloatField(null=True, blank=True)
    effbeam = models.FloatField(null=True, blank=True)
    scale = models.CharField(blank=True, max_length=20)
    ipixel = models.IntegerField(null=True, blank=True)
    npixels = models.IntegerField(null=True, blank=True)
    centerif = models.FloatField(null=True, blank=True)
    bandwidth = models.FloatField(null=True, blank=True)
    distributionboxinput = models.IntegerField(null=True, blank=True)
    if2 = models.FloatField(null=True, blank=True)
    isflippingif2 = models.IntegerField(null=True, blank=True)
    polarization = models.CharField(blank=True, max_length=20)
    usespeciallo = models.IntegerField(null=True, blank=True)
    derotatorangle = models.FloatField(null=True, blank=True)
    derotatorsystem = models.CharField(blank=True, max_length=20)
    class Meta:
        db_table = 'RxReceiversCfg'

class RxBolometerCfg(models.Model):
    receivers = models.ForeignKey(Receivers)
    nchannels = models.IntegerField(null=True, blank=True)
    channel = models.IntegerField(null=True, blank=True)
    gainbolometer = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'RxBolometerCfg'



########################################################################3
## Backends
########################################################################3

from django.db import models

class Backends(models.Model):
    stbknames = models.ForeignKey(stBkNames)
    receivers = models.ForeignKey(Receivers)
    receivers2 = models.ForeignKey(Receivers, null=True, blank=True)
    npart = models.IntegerField(null=True, blank=True)
    resolution = models.FloatField(null=True, blank=True)
    bandwith = models.FloatField(null=True, blank=True)
    fshift = models.FloatField(null=True, blank=True)
    mode = models.CharField(blank=True, max_length=36)
    percentage = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'Backends'

class Basebands(models.Model):
    backends = models.ForeignKey(Backends)
    fskystart = models.FloatField(null=True, blank=True)
    resolutionfrecuency = models.FloatField(null=True, blank=True)
    nchannels = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'Basebands'



########################################################################3
## SwitchingSettings
########################################################################3

from django.db import models

class SwitchingValues(models.Model):
    stswitchingmodes = models.ForeignKey(stSwitchingModes)
    scans = models.ForeignKey(Scans)
    ncycles = models.IntegerField(null=True, blank=True)
    nphases = models.IntegerField(null=True, blank=True)
    timeperphase = models.FloatField(null=True, blank=True)
    timepersecond = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'SwitchingValues'

class FrequencySwitching(models.Model):
    receivers = models.ForeignKey(Receivers)
    switchingvalues = models.ForeignKey(SwitchingValues)
    frequencythrow = models.FloatField(null=True, blank=True)
    frequencyoffset1 = models.FloatField(null=True, blank=True)
    frequencyoffset2 = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'FrequencySwitching'



########################################################################3
## ObservationSettings
########################################################################3

from django.db import models

class TipSettings(models.Model):
    scans = models.ForeignKey(Scans)
    tipfrom = models.FloatField(null=True, blank=True)
    tipto = models.FloatField(null=True, blank=True)
    tipby = models.FloatField(null=True, blank=True)
    doslew = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'TipSettings'

class FocusSettings(models.Model):
    scans = models.ForeignKey(Scans)
    len = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'FocusSettings'

class PointingSettings(models.Model):
    scans = models.ForeignKey(Scans)
    len = models.FloatField(null=True, blank=True)
    dodoublebeam = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'PointingSettings'

class OTFMapSettings(models.Model):
    scans = models.ForeignKey(Scans)
    xstart = models.FloatField(null=True, blank=True)
    ystart = models.FloatField(null=True, blank=True)
    xend = models.FloatField(null=True, blank=True)
    yend = models.FloatField(null=True, blank=True)
    reference = models.ForeignKey(Offsets, null=True, blank=True)
    croloop = models.CharField(blank=True, max_length=255)
    xstep = models.FloatField(null=True, blank=True)
    ystep = models.FloatField(null=True, blank=True)
    alternativespeedtotf = models.CharField(blank=True, max_length=45)
    speedstart = models.FloatField(null=True, blank=True)
    speedend = models.FloatField(null=True, blank=True)
    timeperotf = models.FloatField(null=True, blank=True)
    timeperreference = models.FloatField(null=True, blank=True)
    dozigzag = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'OTFMapSettings'

class OnOffSettings(models.Model):
    scans = models.ForeignKey(Scans)
    xoffset = models.FloatField(null=True, blank=True)
    yoffset = models.FloatField(null=True, blank=True)
    reference = models.ForeignKey(Offsets, null=True, blank=True)
    dosymmetric = models.IntegerField(null=True, blank=True)
    doswwobbler = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'OnOffSettings'

class CalibrationSettings(models.Model):
    scans = models.ForeignKey(Scans)
    doambient = models.IntegerField(null=True, blank=True)
    docold = models.IntegerField(null=True, blank=True)
    dosky = models.IntegerField(null=True, blank=True)
    skyoffsets = models.ForeignKey(Offsets, null=True, blank=True)
    gainimagerx = models.ForeignKey(stRxNames, null=True, db_column='gainimagerx', blank=True)
    dogrid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'CalibrationSettings'



########################################################################3
## Antenna
########################################################################3

from django.db import models

class Antenna(models.Model):
    scans = models.ForeignKey(Scans)
    actualaz = models.FloatField(null=True, blank=True)
    actualel = models.FloatField(null=True, blank=True)
    trackaz = models.FloatField(null=True, blank=True)
    trackel = models.FloatField(null=True, blank=True)
    p2 = models.FloatField(null=True, blank=True)
    p4 = models.FloatField(null=True, blank=True)
    p5 = models.FloatField(null=True, blank=True)
    p7 = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'Antenna'


class Secundary(models.Model):
    scans = models.ForeignKey(Scans)
    focuscorrectionx = models.FloatField(null=True, blank=True)
    focuscorrectiony = models.FloatField(null=True, blank=True)
    focuscorrectionz = models.FloatField(null=True, blank=True)
    rotationangle = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'Secundary'



########################################################################3
## Sources
########################################################################3

from django.db import models

class SourceRadialVelocities(models.Model):
    referenceframe = models.CharField(max_length=45)
    convention = models.CharField(max_length=45)
    velocity = models.FloatField(null=True, blank=True)
    xoffsetdoppler = models.FloatField(null=True, blank=True)
    yoffsetdoppler = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'SourceRadialVelocities'

class PredefinedSources(models.Model):
    projects = models.ForeignKey(Projects)
    sourceradialvelocities = models.ForeignKey(SourceRadialVelocities)
    sourcename = models.CharField(max_length=255)
    basissystem = models.CharField(blank=True, max_length=45)
    equinoxsystem = models.CharField(blank=True, max_length=20)
    equinoxyear = models.FloatField(null=True, blank=True)
    lambda_field = models.FloatField(db_column='lambda') # Field renamed because it was a Python reserved word.
    beta = models.FloatField()
    priority = models.FloatField()
    aimedrms = models.FloatField()
    actualrms = models.FloatField(null=True, blank=True)
    flux = models.FloatField(null=True, blank=True)
    sourcecomment = models.TextField(blank=True)
    class Meta:
        db_table = 'PredefinedSources'

class ObservedSources(models.Model):
    sourceradialvelocities = models.ForeignKey(SourceRadialVelocities)
    scans = models.ForeignKey(Scans)
    sourcename = models.CharField(max_length=255)
    basissystem = models.CharField(blank=True, max_length=45)
    equinoxsystem = models.CharField(blank=True, max_length=20)
    equinoxyear = models.FloatField(null=True, blank=True)
    lambda_field = models.FloatField(db_column='lambda') # Field renamed because it was a Python reserved word.
    beta = models.FloatField()
    descriptivesystem = models.CharField(blank=True, max_length=45)
    alphad = models.FloatField(null=True, blank=True)
    betad = models.FloatField(null=True, blank=True)
    gammad = models.FloatField(null=True, blank=True)
    projection = models.CharField(blank=True, max_length=45)
    lambdaprojection = models.FloatField(null=True, blank=True)
    betaprojection = models.FloatField(null=True, blank=True)
    kappaprojection = models.FloatField(null=True, blank=True)
    topology = models.CharField(blank=True, max_length=20)
    class Meta:
        db_table = 'ObservedSources'



########################################################################3
## AUX
########################################################################3

from django.db import models

########################################################################3
## Metadata
########################################################################3

class MetadataEntities(models.Model):
    entityname = models.CharField(blank=True, max_length=45)
    class Meta:
        db_table = 'MetadataEntities'

class MetadataAttributes(models.Model):
    metadataentities = models.ForeignKey(MetadataEntities)
    attributename = models.CharField(max_length=45)
    ucd = models.CharField(blank=True, max_length=255)
    unit = models.CharField(blank=True, max_length=20)
    readtype = models.CharField(max_length=21)
    readfrom = models.CharField(max_length=255)
    readwhere = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'MetadataAttributes'



########################################################################3
## Weather
########################################################################3

class WeatherStation(models.Model):
    timestamp = models.DateTimeField()
    electricalfield = models.FloatField(null=True, blank=True)
    windvel = models.FloatField(null=True, blank=True)
    windvelmax = models.FloatField(null=True, blank=True)
    winddir = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'WeatherStation'

class WeatherTau(models.Model):
    timestamp = models.DateTimeField(null=True, blank=True)
    tau = models.FloatField(null=True, blank=True)
    sigma = models.FloatField(null=True, blank=True)
    fit = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'WeatherTau'



########################################################################3
## Telescope Status
########################################################################3

class telescopeStatus(models.Model):
    sttelescopestates = models.ForeignKey(stTelescopeStates)
    timestamp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'telescopeStatus'



########################################################################3
## Pools
########################################################################3

class Pools(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(blank=True, max_length=255)
    projects = models.ManyToManyField(db_table = "Pools_has_Projects") # Automatically generated!
    class Meta:
        db_table = 'Pools'

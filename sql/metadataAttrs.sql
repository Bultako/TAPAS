begin;

-- attributeName: Name of the attribute in the Datamodel
-- UCD: UCD of the attribute
-- Unit: Physical unit of the attribute (empty if no unit),
-- readType: Elvin | PakoXML | MiraXML | FITS
-- readFrom
INSERT INTO `MetadataAttributes` (`attributeName`, `UCD`, `UType`, `Unit`, `readType`, `readFrom`, `readWhere`, `description`, `MetadataEntity_id`) VALUES

#class Antenna(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('actualAz',    '',     '',     '',     '',         '',         '',         '',                 32),
    ('actualEl',    '',     '',     '',     '',         '',         '',         '',                 32),
    ('trackAz',     '',     '',     '',     '',         '',         '',         '',                 32),
    ('trackEl',     '',     '',     '',     '',         '',         '',         '',                 32),
    ('p2',          '',     '',     'rad',  '',         '',         '',         '',                 32),
    ('p4',          '',     '',     'rad',  '',         '',         '',         '',                 32),
    ('p5',          '',     '',     'rad',  '',         '',         '',         '',                 32),
    ('p7',          '',     '',     'rad',  '',         '',         '',         '',                 32),

#class Secundary(models.Model),:
    # name                 UCD     UType   Unit    readType    readFrom    readWhere   description
    ('focusCorrectionX',    '',     '',     'mm',   '',         '',         '',         '',                 33),
    ('focusCorrectionY',    '',     '',     'mm',   '',         '',         '',         '',                 33),
    ('focusCorrectionZ',    '',     '',     'mm',   '',         '',         '',         '',                 33),
    ('rotationAngle',       '',     '',     'rad',  '',         '',         '',         '',                 33),


#class Backend(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('nPart',       '',     '',     '-',    '',         '',         '',         '',                 22),
    ('resolution',  '',     '',     'GHz',  '',         '',         '',         '',                 22),
    ('bandwith',    '',     '',     'GHz',  '',         '',         '',         '',                 22),
    ('fShift',      '',     '',     'GHz',  '',         '',         '',         '',                 22),
    ('mode',        '',     '',     '-',    '',         '',         '',         '',                 22),
    ('percentage',  '',     '',     '-',    '',         '',         '',         '',                 22),
    
#class Baseband(models.Model),:
    # name                 UCD     UType   Unit    readType    readFrom    readWhere   description
    ('fSkyStart',           '',     '',     'GHz',  '',         '',         '',         '',                 23), #GHz??
    ('resolutionFrecuency', '',     '',     'GHz',  '',         '',         '',         '',                 23), #GHz??
    ('nChannels',           '',     '',     '-',    '',         '',         '',         '',                 23),
    
#class TipSettings(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('tipFrom',     '',     '',     '-',    '',         '',         '',         'Airmass Start',                 26),
    ('tipTo',       '',     '',     '-',    '',         '',         '',         'Airmass End',                 26),
    ('tipBy',       '',     '',     '-',    '',         '',         '',         'Airmass step',                 26),
    ('doSlew',      '',     '',     '-',    '',         '',         '',         'Do Slew',                 26),

#class FocusSettings(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('len',        '',     '',     'mm',   '-',        '',         '',         '',                         27),

#class PointingSettings(models.Model),:
    # name          UCD     UType   Unit    readType    readFrom    readWhere   description
    ('len',          '',     '',     'rad',  '-',        '',         '',         '',                 28),
    ('doDoubleBeam', '',     '',     '-',    '',         '',         '',         'Do double-beam pointing',                 28),

#class OTFMapSettings(models.Model),:
    # name                 UCD     UType   Unit    readType    readFrom    readWhere   description
    ('xStart',              '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('yStart',              '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('xEnd',                '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('yEnd',                '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('croLoop',             '',     '-',    '',      '',         '',         '',         'Sequence of "R" (off-source Reference), or "O" (on-source OTF),. E.g. "ROOR"',                 29),
    ('xStep',               '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('yStep',               '',     '',     'rad',   '',         '',         '',         '',                 29),
    ('alternativeSpeedTotf','',     '',     '',      '',         '',         '',         '',                 29), #Unit??
    ('speedStart',          '',     '',     'rad/s', '',         '',         '',         '',                 29),
    ('speedEnd',            '',     '',     'rad/s', '',         '',         '',         '',                 29),
    ('timePerOtf',          '',     '',     's',     '',         '',         '',         '',                 29),
    ('timePerReference',    '',     '',     's',     '',         '',         '',         '',                 29),
    ('doZigzag',            '',     '',     '-',     '',         '',         '',         '',                 29),

#class OnOffSettings(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('xOffset',     '',     '',     '',      '',         '',         '',         'x-Offset of "on-source" position',                 30),
    ('yOffset',     '',     '',     '',      '',         '',         '',         'y-Offset of "on-source" position',                 30),
    ('doSymmetric', '',     '',     '-',     '',         '',         '',         'Do symmetric',                 30),
    ('doSwWobbler', '',     '',     '-',     '',         '',         '',         'Do wobbler switching',                 30),

#class CalibrationSettings(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('doAmbient',   '',     '',     '-',     '',         '',         '',         'Do ambient subscan',                 31),
    ('doCold',      '',     '',     '-',     '',         '',         '',         'Do cold subscan',                 31),
    ('doSky',       '',     '',     '-',     '',         '',         '',         'Do sky subscan',                 31),
    ('doGrid',      '',     '',     '-',     '',         '',         '',         'Do grid',                 31),


#class WeatherStation(models.Model),:
    # name             UCD     UType   Unit    readType    readFrom    readWhere   description
    ('timeStamp',       '',     '',     '-',    '',         '',         '',         '',                 37),
    ('electricalField', '',     '',     '',     '',         '',         '',         '',                 37),
    ('windVel',         '',     '',     '',     '',         '',         '',         'Wind velocity',                 37), #m/s?
    ('windVelMax',      '',     '',     '',     '',         '',         '',         'Maximum wind velocity',                 37), #m/s?
    ('windDir',         '',     '',     '',     '',         '',         '',         'Wind direction',                 37),
    ('humidity',        '',     '',     '',     '',         '',         '',         '',                 37),
    ('pressure',        '',     '',     '',     '',         '',         '',         '',                 37),
    ('temperature',     '',     '',     '',     '',         '',         '',         '',                 37), #ºC?

#class WeatherTau(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('timeStamp',   '',     '',     '-',    '',         '',         '',         '',                 38),
    ('tau',         '',     '',     '',     '',         '',         '',         '',                 38),
    ('sigma',       '',     '',     '',     '',         '',         '',         '',                 38),
    ('fit',         '',     '',     '',     '',         '',         '',         '',                 38),

/*
#class TelescopeStatus(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('timeStamp',   '',     '',     '-',    '',         '',         '',         ''),

#class Pool(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name',      '',     '',     '-',    '',         '',         '',         ''),
    ('description', '',     '',     '-',    '',         '',         '',         ''),
    ('projects',  '',     '',     '-',    '',         '',         '',         ''), generated!

#class PoolPeriod(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('startDate', '',     '',     '-',    '',         '',         '',         ''),
    ('endDate',   '',     '',     '-',    '',         '',         '',         ''),

#class PredefinedReceiver(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('receiverComment', '', '', 'models.TextField("Comment", blank=True),

#class Receiver(models.Model),:
*/

#class RxReceiverCfg(models.Model),:
    # name             UCD     UType   Unit    readType    readFrom    readWhere   description
    ('lineName',        '',     '',     '-',    '',         '',         '',         '',                 20),
    ('frequency',       '',     '',     'GHz',  '',         '',         '',         '',                 20),
    ('sideBand',        '',     '',     '-',    '',         '',         '',         '',                 20),
    ('doppler',         '',     '',     '-',    '',         '',         '',         'Doppler correction',                 20),
    ('width',           '',     '',     '-',    '',         '',         '',         '',                 20),
    ('gainImage',       '',     '',     '-',    '',         '',         '',         '',                 20),
    ('tempCold',        '',     '',     'K',    '',         '',         '',         '',                 20),
    ('tempAmbient',     '',     '',     'K',    '',         '',         '',         '',                 20),
    ('effForward',      '',     '',     '-',    '',         '',         '',         'Forward Efficiency',                 20),
    ('effBeam',         '',     '',     '-',    '',         '',         '',         'Beam Efficiency',                 20),
    ('scale',           '',     '',     '-',    '',         '',         '',         'Forward Efficiency',                 20),
    ('iPixel',          '',     '',     '-',    '',         '',         '',         'Selected pixel',                 20),
    ('nPixels',         '',     '',     '-',    '',         '',         '',         '# of pixels',                 20),
    ('centerIF',        '',     '',     'GHz',  '',         '',         '',         '',                 20),
    ('bandwidth',       '',     '',     'GHz',  '',         '',         '',         '',                 20),
    ('IF2',             '',     '',     'GHz',  '',         '',         '',         '',                 20),
    ('isFlippingIF2',   '',     '',     '-',    '',         '',         '',         'Is flipping IF2?',                 20),
    ('polarization',    '',     '',     '-',    '',         '',         '',         '',                 20),
    ('useSpecialLO',    '',     '',     '-',    '',         '',         '',         'Use special LO?',                 20),
    ('derotatorAngle',  '',     '',     'rad',  '',         '',         '',         'Derotator angle for HERA',                 20),
    ('derotatorSystem', '',     '',     '-',    '',         '',         '',         'Derotator system for HERA',                 20),
    # name                   UCD     UType   Unit    readType    readFrom    readWhere   description
    ('distributionBoxInput', '',     '',     '-',    '',         '',         '',         'Distribution-Box Input',                 20),
    

#class RxBolometerCfg(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('nChannels',     '',     '',     '-',    '',         '',         '',         '',                 21),
    ('channel',       '',     '',     '-',    '',         '',         '',         '',                 21),
    ('gainBolometer', '',     '',     '-',    '',         '',         '',         '',                 21),

#class Offset(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('xOffset',     '',     '',     'rad', '',         '',         '',         '',                 13),
    ('yOffset',     '',     '',     'rad', '',         '',         '',         '',                 13),

#class Project(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
/*    ('projectId', '', '', 'models.IntegerField("Project ID", null=True, blank=True),
    ('title', '', '', 'models.CharField(blank=True, max_length=255),
    ('priority', '', '', 'models.IntegerField(null=True, blank=True), #a.k.a. HERA projectStatus
    ('ranking', '', '', 'models.IntegerField(null=True, blank=True), #a.k.a. HERA grade
    ('allocatedTime', '', '', 'models.FloatField("Allocated Time", null=True, blank=True, help_text="Unit=hours"),
    ('usedTime', '', '', 'models.FloatField("Used Time", null=True, blank=True, help_text="Unit=hours"),
    ('requiredOpacity', '', '', 'models.FloatField("Required Opacity", null=True, blank=True),
    ('requiredWaterVapor', '', '', 'models.FloatField("Required Water vapor", null=True, blank=True, help_text="Unit=mm"),
    ('requiredSkynoise', '', '', 'models.CharField("Required Skynoise", blank=True, max_length=18),
    ('weatherComment', '', '', 'models.TextField("Weather Comment", blank=True),
    ('projectModes', '', '', 'models.ManyToManyField(stProjectModes, 
    ('projectComment', '', '', 'models.TextField("Project Comment", blank=True),
    ('projectBriefComment', '', '', 'models.TextField("Project Brief Comment", blank=True),
    ('projectRemarkComment', '', '', 'models.TextField("Project Remark Comment", blank=True, help_text="For admin"),
*/
#class Scan(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('ncsId',       '',     '',     '-',    '',         '',         '',         '',                 15),
    ('startTime',   '',     '',     '-',    '',         '',         '',         '',                 15),
    ('endTime',     '',     '',     '-',    '',         '',         '',         '',                 15),
    ('LST',         '',     '',     '',     '',         '',         '',         '',                 15),
    ('MJD',         '',     '',     '',     '',         '',         '',         '',                 15),
    ('nSubscans',   '',     '',     '-',    '',         '',         '',         '# of subscans',                 15),
    ('tSubscans',   '',     '',     's',    '',         '',         '',         'Subscan time',                 15),

#not clear yet if it's going to be used this #class or
#a comment extension for Django!
#class ScanComment(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
#    ('extraComment', '', '', 'models.TextField("Extra comment", blank=True),

#class SourceRadialVelocity(models.Model),:
    # name             UCD     UType   Unit    readType    readFrom    readWhere   description
    ('referenceFrame',  '',     '',     '-',    '',         '',         '',         'Reference system',                 34),
    ('convention',      '',     '',     '-',    '',         '',         '',         '',                 34),
    ('velocity',        '',     '',     'm/s',  '',         '',         '',         '',                 34),
    ('xOffsetDoppler',  '',     '',     'rad',  '',         '',         '',         'x-Offset Doppler',                 34),
    ('yOffsetDoppler',  '',     '',     'rad',  '',         '',         '',         'y-Offset Doppler',                 34),

/*
#class PredefinedSources(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('sourceName', '', '', 'models.CharField("Source name", max_length=255),
    ('basisSystem', '', '', 'models.CharField("Basis system", blank=True, max_length=45, choices=BASISSYSTEM_CHOICES),
    ('equinoxSystem', '', '', 'models.CharField("Equinox system", blank=True, max_length=20),
    ('equinoxYear', '', '', 'models.FloatField("Equinox year", null=True, blank=True, help_text="Unit=year"),
    ('lambdaField', '', '', 'models.FloatField("Lambda", db_column='lambda', null=True, blank=True, help_text="Unit=rad (RA),"),
    ('beta', '', '', 'models.FloatField("Beta", null=True, blank=True, help_text="Unit=rad (Decl),"),
    ('priority', '', '', 'models.FloatField("Priority", null=True, blank=True),
    ('aimedRMS', '', '', 'models.FloatField("Aimed RMS", null=True, blank=True, help_text="Unit=mJy"),
    ('actualRMS', '', '', 'models.FloatField("Actual RMS", null=True, blank=True, help_text="Unit=mJy"),
    ('resolution', '', '', 'models.FloatField("Resolution", null=True, blank=True, help_text="Unit=Km/s"),
    ('flux', '', '', 'models.FloatField("Flux", null=True, blank=True, help_text="Unit=mJy"),
    ('sourceComment', '', '', 'models.TextField("Comment", blank=True, null=True),
*/
#class ObservedSources(models.Model),:
    # name             UCD     UType   Unit    readType    readFrom    readWhere   description
    ('sourceName',      '',     '',     '-',    '',         '',         '',         '',                 36),
    ('basisSystem',     '',     '',     '-',    '',         '',         '',         '',                 36),
    ('equinoxSystem',   '',     '',     '-',    '',         '',         '',         '',                 36),
    ('equinoxYear',     '',     '',     'year', '',         '',         '',         '',                 36),
    ('lambdaField',     '',     '',     'rad',  '',         '',         '',         'RA',                 36),
    ('beta',            '',     '',     'rad',  '',         '',         '',         'Decl',                 36),
    ('descriptiveSystem','',    '',     '-',    '',         '',         '',         '',                 36),
    ('alphaD',          '',     '',     'rad',  '',         '',         '',         '',                 36),
    ('betaD',           '',     '',     'rad',  '',         '',         '',         '',                 36),
    ('gammaD',          '',     '',     'rad',  '',         '',         '',         '',                 36),
    ('projection',      '',     '',     '-',    '',         '',         '',         '',                 36),
    ('lambdaProjection', '',    '',     'rad',  '',         '',         '',         '',                 36),
    ('betaProjection',  '',     '',     'rad',  '',         '',         '',         '',                 36),
    ('kappaProjection', '',     '',     'rad',  '',         '',         '',         '',                 36),
    ('topology',        '',     '',     '-',    '',         '',         '',         '',                 36),
    ('sourceComment',   '',     '',     '-',    '',         '',         '',         '',                 36),


/*#class stPredefinedComments(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('comment_text', '', '', 'models.TextField("Comment", blank=True),
    ('technical', '', '', 'models.BooleanField(null=True, blank=True),
*/

#class stPointingModels(models.Model),:
# UNITS ??
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('timeStamp',   '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p1',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p2',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p3',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p4',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p5',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p7',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p8',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('p9',          '',     '',     '',    '',         '',         '',         '',                 2), #rad?
    ('rxho',        '',     '',     '',    '',         '',         '',         'rxHorizontal',                 2),
    ('rxve',        '',     '',     '',    '',         '',         '',         'rxVertical',                 2),
    ('refract3',    '',     '',     '',    '',         '',         '',         '',                 2),
    
    # name                     UCD     UType   Unit    readType    readFrom    readWhere   description    
    ('subref_rotationzero',     '',     '',     '',    '',         '',         '',         '',                 2),
    ('subref_rotationphi0',     '',     '',     '',    '',         '',         '',         '',                 2),
    ('subref_rotationradius',   '',     '',     '',    '',         '',         '',         '',                 2),
    ('encoder_sincol',          '',     '',     '',    '',         '',         '',         '',                 2),
    ('encoder_coscol',          '',     '',     '',    '',         '',         '',         '',                 2),

/*#class stRxNames(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=20),
    ('description', '', '', 'models.TextField(blank=True),

#class stProjectModes(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=45),
    ('description', '', '', 'models.CharField(blank=True, max_length=255),

#class stBkNames(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=20),
    ('description', '', '', 'models.TextField(blank=True),

#class stObservingModes(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=45),
    ('description', '', '', 'models.TextField(blank=True),

#class stFileLocations(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('locationname', '', '', 'models.CharField(blank=True, max_length=45),
    ('hostname', '', '', 'models.CharField(blank=True, max_length=45),
    ('path', '', '', 'models.CharField(blank=True, max_length=255),

#class stTelescopeStates(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=255),
    ('description', '', '', 'models.TextField(blank=True),

#class stSwitchingModes(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=45),
    ('description', '', '', 'models.TextField(blank=True),

#class stSystemNames(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('name', '', '', 'models.CharField(blank=True, max_length=45),
    ('description', '', '', 'models.TextField(blank=True),
*/
#class stSoftwareVersions(models.Model),:
    # name         UCD     UType   Unit    readType    readFrom    readWhere   description
    ('software',   '',     '',     '-',    '',         '',         '',         'Software Package Name', 3),
    ('version',    '',     '',     '-',    '',         '',         '',         'Version', 3),
    ('date',       '',     '',     '-',    '',         '',         '',         'Date when version was released', 3),
    ('description','',     '',     '-',    '',         '',         '',         'Software description', 3),

#class SwitchingCfg(models.Model),:
    # name             UCD     UType   Unit    readType    readFrom    readWhere   description
    ('nCycles',         '',     '',     '-',    '',         '',         '',         'Number of cycles',                 24),
    ('nPhases',         '',     '',     '-',    '',         '',         '',         'Number of phases',                 24),
    ('timePerPhase',    '',     '',     's',    '',         '',         '',         '',                 24),
    ('timePerSecond',   '',     '',     's',    '',         '',         '',         '',                 24),

#class FrequencySwitching(models.Model),:
    # name                 UCD     UType   Unit    readType    readFrom    readWhere   description
    ('frequencyThrow',      '',     '',     'GHz',  '',         '',         '',         '',                 25),
    ('frequencyOffset1',    '',     '',     'GHz',  '',         '',         '',         '',                 25),
    ('frequencyOffset2',    '',     '',     'GHz',  '',         '',         '',         '',                 25);

commit;
#rollback;

-- ------------------------------------------------------------
-- Static table with the pointing model when updated. Read them from Elvin!
-- ------------------------------------------------------------

CREATE TABLE stPointingModels (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  p1 FLOAT NULL,
  p2 FLOAT NULL,
  p3 FLOAT NULL,
  p4 FLOAT NULL,
  p5 FLOAT NULL,
  p7 FLOAT NULL,
  p8 FLOAT NULL,
  p9 FLOAT NULL,
  rxho FLOAT NULL,
  rxve FLOAT NULL,
  refract3 FLOAT NULL,
  subref_rotationZero FLOAT NULL,
  subref_rotationPhi0 FLOAT NULL,
  subref_rotationRadius FLOAT NULL,
  encoder_sinCol FLOAT NULL,
  encoder_cosCol FLOAT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- List of pools: S06, W06, HeraS06, HeraW07...
-- ------------------------------------------------------------

CREATE TABLE Pools (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- For the bolopool:
-- -BoloMap
-- -BoloOnOff
-- -SIS
-- 
-- For the hera pool?
-- ------------------------------------------------------------

CREATE TABLE stProjectModes (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  description VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- In the predefinedComment, should be needed a "default" predefined comment, like a "null" comment.
-- ------------------------------------------------------------

CREATE TABLE stPredefinedComments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  comment_text TEXT NULL,
  technical BOOL NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Static table with all the Observing Modes:
-- calibrate
-- pointing
-- focus
-- tip
-- onOff
-- onTheFlyMap
-- track
-- VLBI
-- ------------------------------------------------------------

CREATE TABLE stObservingModes (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  description VARCHAR(45) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE SourceRadialVelocities (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  referenceFrame VARCHAR(45) NOT NULL,
  convention VARCHAR(45) NOT NULL,
  velocity DOUBLE NULL,
  xOffsetDoppler FLOAT NULL,
  yOffsetDoppler FLOAT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Table with all the Astronomers known. Special atention to sync with Clemens database, and with name convention (WikiName?) Under discussion.
-- ------------------------------------------------------------

CREATE TABLE Users (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  fullname VARCHAR(255) NULL,
  email VARCHAR(45) NULL,
  institute VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Static table with the available file locations. In the "path" varchar, tags could be used, e.g. "/vis/{PRJ_ID}/observationData/{YYYYMM}"
-- 
-- Notice this table is not related with Scan. Scan will kept the filename attribute and the path to this file will be build on the fly using FileLocations table and the IP of the user.
-- ------------------------------------------------------------

CREATE TABLE stFileLocations (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  locationName VARCHAR(45) NULL,
  hostname VARCHAR(45) NULL,
  path VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE stBkNames (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(20) NULL,
  description VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE stRxNames (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(20) NULL,
  description VARCHAR(255) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- The telescope states could be (initially):
-- -Hera
-- -Bolometer
-- -Heterodyne
-- -Technical Problem
-- -Bad weather
-- -Maintenance
-- ------------------------------------------------------------

CREATE TABLE stTelescopeStates (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  state VARCHAR(255) NULL,
  description TEXT NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- From Elvin notice message: weatherStation:data 
-- ------------------------------------------------------------

CREATE TABLE WeatherStation (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  timeStamp DATETIME NOT NULL,
  electricalField FLOAT NULL,
  windVel FLOAT NULL,
  windVelMax FLOAT NULL,
  windDir FLOAT NULL,
  humidity FLOAT NULL,
  pressure FLOAT NULL,
  temperature FLOAT NULL,
  PRIMARY KEY(id),
  UNIQUE INDEX WeatherStation_timeStamp(timeStamp)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- From Elvin info message: weather:tau
-- ------------------------------------------------------------

CREATE TABLE WeatherTau (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  timeStamp DATETIME NULL,
  tau FLOAT NULL,
  sigma FLOAT NULL,
  fit FLOAT NULL,
  PRIMARY KEY(id),
  UNIQUE INDEX WeatherTau_timeStamp(timeStamp)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- systemName for reference:
-- 
-- horizontalTrue
-- ¿horizontal?
-- projection
-- nasmyth
-- ------------------------------------------------------------

CREATE TABLE stSystemNames (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Static table with the different software versions.
-- ------------------------------------------------------------

CREATE TABLE stSoftwareVersions (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  software VARCHAR(45) NOT NULL,
  version VARCHAR(20) NOT NULL,
  date DATETIME NULL,
  PRIMARY KEY(id),
  UNIQUE INDEX softwareVersions_uniqueswVer(software, version)
)
TYPE=InnoDB;

CREATE TABLE MetadataEntities (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  entityName VARCHAR(45) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Static table with all the Switching Modes:
-- totalPower
-- beamSwitching
-- wobblerSwitching
-- frequencySwitching
-- ------------------------------------------------------------

CREATE TABLE stSwitchingModes (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  description VARCHAR(45) NULL,
  PRIMARY KEY(id)
)
TYPE=InnoDB;

CREATE TABLE telescopeStatus (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  stTelescopeStates_id INTEGER UNSIGNED NOT NULL,
  timeStamp DATETIME NULL,
  PRIMARY KEY(id),
  INDEX telescopeStatus_FKIndex1(stTelescopeStates_id),
  FOREIGN KEY(stTelescopeStates_id)
    REFERENCES stTelescopeStates(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE MetadataAttributes (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  MetadataEntities_id INTEGER UNSIGNED NOT NULL,
  attributeName VARCHAR(45) NOT NULL,
  UCD VARCHAR(255) NULL,
  Unit VARCHAR(20) NULL,
  readType ENUM('elvin','pakoxml','miraxml','fits') NOT NULL,
  readFrom VARCHAR(255) NOT NULL,
  readWhere VARCHAR(255) NOT NULL,
  description TEXT NULL,
  PRIMARY KEY(id),
  INDEX MetadataAttributes_FKIndex1(MetadataEntities_id),
  FOREIGN KEY(MetadataEntities_id)
    REFERENCES MetadataEntities(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Offsets (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  system_id INTEGER UNSIGNED NOT NULL,
  xOffset FLOAT NULL,
  yOffset FLOAT NULL,
  PRIMARY KEY(id),
  INDEX Offsets_FKIndex1(system_id),
  FOREIGN KEY(system_id)
    REFERENCES stSystemNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Projects (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Observer_id INTEGER UNSIGNED NOT NULL,
  PI_id INTEGER UNSIGNED NOT NULL,
  projectID INTEGER UNSIGNED NULL,
  title VARCHAR(255) NULL,
  priority INTEGER UNSIGNED NULL,
  ranking INTEGER UNSIGNED NULL,
  allocatedTime FLOAT NULL,
  usedTime FLOAT NULL,
  projectComment TEXT NULL,
  requiredOpacity FLOAT NULL,
  requiredSkynoise ENUM('low','medium','high') NULL,
  weatherComment TEXT NULL,
  PRIMARY KEY(id),
  INDEX Project_FKIndex1(PI_id),
  INDEX Projects_projectID(projectID),
  INDEX Projects_FKIndex2(Observer_id),
  FOREIGN KEY(PI_id)
    REFERENCES Users(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Observer_id)
    REFERENCES Users(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Scans (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  system_id INTEGER UNSIGNED NULL,
  stObservingModes_id INTEGER UNSIGNED NOT NULL,
  stPointingModels_id INTEGER UNSIGNED NOT NULL,
  Projects_id INTEGER UNSIGNED NOT NULL,
  ncsID INTEGER UNSIGNED NULL,
  startTime DATETIME NULL,
  endTime DATETIME NULL,
  LST FLOAT NULL,
  MJD FLOAT NULL,
  nSubscans INTEGER UNSIGNED NULL,
  tSubscans FLOAT NULL,
  PRIMARY KEY(id),
  INDEX Scan_FKIndex1(Projects_id),
  INDEX Scan_FKIndex3(stPointingModels_id),
  INDEX Scan_FKIndex4(stObservingModes_id),
  INDEX Scans_ncsID(ncsID),
  INDEX Scans_FKIndex4(system_id),
  FOREIGN KEY(Projects_id)
    REFERENCES Projects(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stPointingModels_id)
    REFERENCES stPointingModels(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(stObservingModes_id)
    REFERENCES stObservingModes(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(system_id)
    REFERENCES stSystemNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE TipSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  tipFrom FLOAT NULL,
  tipTo FLOAT NULL,
  tipBy FLOAT NULL,
  doSlew BOOL NULL,
  PRIMARY KEY(id),
  INDEX TipSettings_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Just in case.
-- ------------------------------------------------------------

CREATE TABLE Subscans (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  timePerSubscan FLOAT NULL,
  PRIMARY KEY(id),
  INDEX Subscan_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Secundary (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  focusCorrectionX DOUBLE NULL,
  focusCorrectionY DOUBLE NULL,
  focusCorrectionZ DOUBLE NULL,
  rotationAngle FLOAT NULL,
  PRIMARY KEY(id),
  INDEX Secundary_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE PointingSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  len FLOAT NULL,
  doDoubleBeam BOOL NULL,
  PRIMARY KEY(id),
  INDEX PointingSettings_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- p2 & p7: observer input pointing corrections
-- p4 & p5: inclinometers
-- ------------------------------------------------------------

CREATE TABLE Antenna (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  actualAz FLOAT NULL,
  actualEl FLOAT NULL,
  trackAz FLOAT NULL,
  trackEl FLOAT NULL,
  p2 DOUBLE NULL,
  p4 DOUBLE NULL,
  p5 DOUBLE NULL,
  p7 DOUBLE NULL,
  PRIMARY KEY(id),
  INDEX Antenna_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE FocusSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  len FLOAT NULL,
  PRIMARY KEY(id),
  INDEX FocusSettings_FKIndex1(Scans_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Projects_has_stProjectModes (
  Projects_id INTEGER UNSIGNED NOT NULL,
  stProjectModes_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(Projects_id, stProjectModes_id),
  INDEX Projects_has_stProjectModes_FKIndex1(Projects_id),
  INDEX Projects_has_stProjectModes_FKIndex2(stProjectModes_id),
  FOREIGN KEY(Projects_id)
    REFERENCES Projects(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stProjectModes_id)
    REFERENCES stProjectModes(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- Please notice this is not a Source Catalog!
-- One scan integrates on a source, so a row with the source is store for each scan. Should be the same sources as specified in the PredefinedSources, but we don't have any constraints about it (observer freedom)
-- ------------------------------------------------------------

CREATE TABLE ObservedSources (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  SourceRadialVelocities_id INTEGER UNSIGNED NOT NULL,
  Scans_id INTEGER UNSIGNED NOT NULL,
  sourceName VARCHAR(255) NOT NULL,
  basisSystem VARCHAR(45) NULL,
  equinoxSystem VARCHAR(20) NULL,
  equinoxYear DOUBLE NULL,
  lambda DOUBLE NOT NULL,
  beta DOUBLE NOT NULL,
  descriptiveSystem VARCHAR(45) NULL,
  alphaD DOUBLE NULL,
  betaD DOUBLE NULL,
  gammaD DOUBLE NULL,
  projection VARCHAR(45) NULL,
  lambdaProjection DOUBLE NULL,
  betaProjection DOUBLE NULL,
  kappaProjection DOUBLE NULL,
  topology VARCHAR(20) NULL,
  PRIMARY KEY(id),
  INDEX Sources_FKIndex1(Scans_id),
  INDEX ObservedSources_FKIndex2(SourceRadialVelocities_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(SourceRadialVelocities_id)
    REFERENCES SourceRadialVelocities(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE SwitchingValues (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  stSwitchingModes_id INTEGER UNSIGNED NOT NULL,
  Scans_id INTEGER UNSIGNED NOT NULL,
  nCycles INTEGER UNSIGNED NULL,
  nPhases INTEGER UNSIGNED NULL,
  timePerPhase FLOAT NULL,
  timePerSecond FLOAT NULL,
  PRIMARY KEY(id),
  INDEX SwitchingValues_FKIndex1(Scans_id),
  INDEX SwitchingValues_FKIndex2(stSwitchingModes_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stSwitchingModes_id)
    REFERENCES stSwitchingModes(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Receivers (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  stRxNames_id INTEGER UNSIGNED NOT NULL,
  Scans_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(id),
  INDEX Receiver_FKIndex1(Scans_id),
  INDEX Receivers_FKIndex2(stRxNames_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stRxNames_id)
    REFERENCES stRxNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- General offsets specified in the <RESOURCE name="offsets">, in PaKo XML
-- ------------------------------------------------------------

CREATE TABLE Scans_has_Offsets (
  Scans_id INTEGER UNSIGNED NOT NULL,
  Offsets_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(Scans_id, Offsets_id),
  INDEX Scans_has_Offsets_FKIndex1(Scans_id),
  INDEX Scans_has_Offsets_FKIndex2(Offsets_id),
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(Offsets_id)
    REFERENCES Offsets(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Pools_has_Projects (
  Pools_id INTEGER UNSIGNED NOT NULL,
  Projects_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(Pools_id, Projects_id),
  INDEX Pools_has_Projects_FKIndex1(Pools_id),
  INDEX Pools_has_Projects_FKIndex2(Projects_id),
  FOREIGN KEY(Pools_id)
    REFERENCES Pools(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Projects_id)
    REFERENCES Projects(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE PredefinedReceivers (
  Projects_id INTEGER UNSIGNED NOT NULL,
  stRxNames_id INTEGER UNSIGNED NOT NULL,
  commentsReceiver TEXT NULL,
  PRIMARY KEY(Projects_id, stRxNames_id),
  INDEX Projects_has_stRxNames_FKIndex1(Projects_id),
  INDEX Projects_has_stRxNames_FKIndex2(stRxNames_id),
  FOREIGN KEY(Projects_id)
    REFERENCES Projects(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stRxNames_id)
    REFERENCES stRxNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

-- ------------------------------------------------------------
-- This is a source catalog for the Project. It is based on the sources specified on the project proposal.
-- 
-- NOTE: aimedRMS & actualRMS are in mJy in the Pool DB -> Jy
-- ------------------------------------------------------------

CREATE TABLE PredefinedSources (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Projects_id INTEGER UNSIGNED NOT NULL,
  SourceRadialVelocities_id INTEGER UNSIGNED NOT NULL,
  sourceName VARCHAR(255) NOT NULL,
  basisSystem VARCHAR(45) NULL,
  equinoxSystem VARCHAR(20) NULL,
  equinoxYear DOUBLE NULL,
  lambda DOUBLE NOT NULL,
  beta DOUBLE NOT NULL,
  priority FLOAT NOT NULL,
  aimedRMS FLOAT NOT NULL,
  actualRMS FLOAT NULL,
  flux FLOAT NULL,
  sourceComment TEXT NULL,
  PRIMARY KEY(id),
  INDEX PredefinedSources_FKIndex1(SourceRadialVelocities_id),
  INDEX PredefinedSources_FKIndex2(Projects_id),
  FOREIGN KEY(SourceRadialVelocities_id)
    REFERENCES SourceRadialVelocities(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Projects_id)
    REFERENCES Projects(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE stSoftwareVersions_usedin_Scans (
  stSoftwareVersions_id INTEGER UNSIGNED NOT NULL,
  Scans_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(stSoftwareVersions_id, Scans_id),
  INDEX softwareVersions_has_Scan_FKIndex1(stSoftwareVersions_id),
  INDEX softwareVersions_has_Scan_FKIndex2(Scans_id),
  FOREIGN KEY(stSoftwareVersions_id)
    REFERENCES stSoftwareVersions(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE OnOffSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  xOffset FLOAT NULL,
  yOffset FLOAT NULL,
  reference_id INTEGER UNSIGNED NULL,
  doSymmetric BOOL NULL,
  doSwWobbler BOOL NULL,
  PRIMARY KEY(id),
  INDEX OnOffSettings_FKIndex1(reference_id),
  INDEX OnOffSettings_FKIndex2(Scans_id),
  FOREIGN KEY(reference_id)
    REFERENCES Offsets(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE OTFMapSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  xStart FLOAT NULL,
  yStart FLOAT NULL,
  xEnd FLOAT NULL,
  yEnd FLOAT NULL,
  reference_id INTEGER UNSIGNED NULL,
  croLoop VARCHAR(255) NULL,
  xStep FLOAT NULL,
  yStep FLOAT NULL,
  alternativeSpeedTotf VARCHAR(45) NULL,
  speedStart FLOAT NULL,
  speedEnd FLOAT NULL,
  timePerOtf FLOAT NULL,
  timePerReference FLOAT NULL,
  doZigzag BOOL NULL,
  PRIMARY KEY(id),
  INDEX OTFMapSettings_FKIndex1(reference_id),
  INDEX OTFMapSettings_FKIndex2(Scans_id),
  FOREIGN KEY(reference_id)
    REFERENCES Offsets(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE CalibrationSettings (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  doAmbient BOOL NULL,
  doCold BOOL NULL,
  doSky BOOL NULL,
  skyOffsets_id INTEGER UNSIGNED NULL,
  gainImageRx INTEGER UNSIGNED NULL,
  doGrid BOOL NULL,
  PRIMARY KEY(id),
  INDEX Calibrations_FKIndex1(skyOffsets_id),
  INDEX Calibrations_FKIndex2(Scans_id),
  INDEX CalibrationSettings_FKIndex3(gainImageRx),
  FOREIGN KEY(skyOffsets_id)
    REFERENCES Offsets(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(gainImageRx)
    REFERENCES stRxNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Backends (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  stBkNames_id INTEGER UNSIGNED NOT NULL,
  Receivers_id INTEGER UNSIGNED NOT NULL,
  Receivers2_id INTEGER UNSIGNED NULL,
  nPart SMALLINT UNSIGNED NULL,
  resolution DOUBLE NULL,
  bandwith DOUBLE NULL,
  fShift DOUBLE NULL,
  mode ENUM('simple', 'parallel', 'polarization') NULL,
  percentage FLOAT NULL,
  PRIMARY KEY(id),
  INDEX Backend_FKIndex1(Receivers_id),
  INDEX Backends_FKIndex2(stBkNames_id),
  INDEX Backends_FKIndex3(Receivers2_id),
  FOREIGN KEY(Receivers_id)
    REFERENCES Receivers(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(stBkNames_id)
    REFERENCES stBkNames(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Receivers2_id)
    REFERENCES Receivers(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE ScanComments (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Scans_id INTEGER UNSIGNED NOT NULL,
  stPredefinedComments_id INTEGER UNSIGNED NOT NULL,
  Users_id INTEGER UNSIGNED NOT NULL,
  extra_comment TEXT NULL,
  PRIMARY KEY(id),
  INDEX ObsComment_FKIndex1(Users_id),
  INDEX ObsComment_FKIndex2(stPredefinedComments_id),
  INDEX ObsComment_FKIndex3(Scans_id),
  FOREIGN KEY(Users_id)
    REFERENCES Users(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(stPredefinedComments_id)
    REFERENCES stPredefinedComments(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE,
  FOREIGN KEY(Scans_id)
    REFERENCES Scans(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE RxReceiversCfg (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Receivers_id INTEGER UNSIGNED NOT NULL,
  lineName VARCHAR(45) NULL,
  frequency DOUBLE NULL,
  sideBand VARCHAR(20) NULL,
  doppler VARCHAR(20) NULL,
  width VARCHAR(20) NULL,
  gainImage FLOAT NULL,
  tempCold FLOAT NULL,
  tempAmbient FLOAT NULL,
  effForward FLOAT NULL,
  effBeam FLOAT NULL,
  scale VARCHAR(20) NULL,
  iPixel SMALLINT UNSIGNED NULL,
  nPixels SMALLINT UNSIGNED NULL,
  centerIF DOUBLE NULL,
  bandWidth DOUBLE NULL,
  distributionBoxInput SMALLINT UNSIGNED NULL,
  IF2 DOUBLE NULL,
  isFlippingIF2 BOOL NULL,
  polarization VARCHAR(20) NULL,
  useSpecialLO BOOL NULL,
  derotatorAngle DOUBLE NULL,
  derotatorSystem VARCHAR(20) NULL,
  PRIMARY KEY(id),
  INDEX RxHeterodyneCfg_FKIndex1(Receivers_id),
  FOREIGN KEY(Receivers_id)
    REFERENCES Receivers(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE Basebands (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Backends_id INTEGER UNSIGNED NOT NULL,
  fSkyStart FLOAT NULL,
  resolutionFrecuency FLOAT NULL,
  nChannels INTEGER UNSIGNED NULL,
  PRIMARY KEY(id),
  INDEX Basebands_FKIndex1(Backends_id),
  FOREIGN KEY(Backends_id)
    REFERENCES Backends(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE RxBolometerCfg (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Receivers_id INTEGER UNSIGNED NOT NULL,
  nChannels SMALLINT UNSIGNED NULL,
  channel SMALLINT UNSIGNED NULL,
  gainBolometer FLOAT NULL,
  PRIMARY KEY(id),
  INDEX RxMamboCfg_FKIndex1(Receivers_id),
  FOREIGN KEY(Receivers_id)
    REFERENCES Receivers(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;

CREATE TABLE FrequencySwitching (
  Receivers_id INTEGER UNSIGNED NOT NULL,
  SwitchingValues_id INTEGER UNSIGNED NOT NULL,
  frequencyThrow DOUBLE NULL,
  frequencyOffset1 DOUBLE NULL,
  frequencyOffset2 DOUBLE NULL,
  PRIMARY KEY(Receivers_id, SwitchingValues_id),
  INDEX Receivers_has_SwitchingValues_FKIndex1(Receivers_id),
  INDEX Receivers_has_SwitchingValues_FKIndex2(SwitchingValues_id),
  FOREIGN KEY(Receivers_id)
    REFERENCES Receivers(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(SwitchingValues_id)
    REFERENCES SwitchingValues(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
TYPE=InnoDB;



-- 
-- Table structure for table `MetadataAttributes`
-- 

-- CREATE TABLE `MetadataAttributes` (
--  `id` int(11) NOT NULL auto_increment,
--  `metadataEntity_id` int(11) NOT NULL,
--  `attributeName` varchar(45) NOT NULL,
--  `UCD` varchar(255) NOT NULL,
--  `UType` varchar(255) NOT NULL,
--  `unit` varchar(20) NOT NULL,
--  `readType` varchar(21) NOT NULL,
--  `readFrom` varchar(255) NOT NULL,
--  `readWhere` varchar(255) NOT NULL,
--  `description` longtext NOT NULL,
--  PRIMARY KEY  (`id`),
--  KEY `MetadataAttributes_metadataEntity_id` (`metadataEntity_id`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- 
-- Dumping data for table `MetadataAttributes`
-- 


-- --------------------------------------------------------

-- 
-- Table structure for table `MetadataEntities`
-- 

-- CREATE TABLE `MetadataEntities` (
--  `id` int(11) NOT NULL auto_increment,
--  `name` varchar(45) NOT NULL,
--  PRIMARY KEY  (`id`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- 
-- Dumping data for table `MetadataEntities`
-- 

INSERT INTO `MetadataEntities` (`name`) VALUES 
    ('Antenna'),
    ('Secondary'),
    ('Backend'),
    ('Baseband'),
    ('TipSettings'),
    ('FocusSettings'),
    ('PointingSettings'),
    ('OTFMapSettings'),
    ('OnOffSettings'),
    ('CalibrationSettings'),
    ('WeatherStation'),
    ('WeatherTau'),
    ('TelescopeStatus'),
    ('Pool'),
    ('PoolPeriod'),
    ('PredefinedReceiver'),
    ('Receiver'),
    ('RxReceiverCfg'),
    ('RxBolometerCfg'),
    ('Offset'),
    ('Project'),
    ('Scan'),
    ('Subscan'),
    ('ScanComment'),
    ('SourceRadialVelocity'),
    ('PredefinedSources'),
    ('ObservedSources'),
    ('stPredefinedComments'),
    ('stPointingModels'),
    ('stRxNames'),
    ('stProjectModes'),
    ('stBkNames'),
    ('stObservingModes'),
    ('stFileLocations'),
    ('stSoftwareVersions'),
    ('stTelescopeStates'),
    ('stSwitchingModes'),
    ('stSystemNames'),
    ('SwitchingCfg'),
    ('FrequencySwitching');

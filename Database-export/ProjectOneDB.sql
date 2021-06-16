-- MySQL dump 10.13  Distrib 8.0.20, for macos10.15 (x86_64)
--
-- Host: localhost    Database: ProjectOneDB
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Action`
--

DROP TABLE IF EXISTS `Action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Action` (
  `ActionID` int NOT NULL AUTO_INCREMENT,
  `Description` varchar(150) NOT NULL,
  PRIMARY KEY (`ActionID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Action`
--

LOCK TABLES `Action` WRITE;
/*!40000 ALTER TABLE `Action` DISABLE KEYS */;
INSERT INTO `Action` VALUES (1,'consequat enim'),(2,'id ante dictum cursus. Nunc mauris elit,'),(3,'Quisque varius. Nam porttitor scelerisque neque. Nullam nisl.'),(4,'nisi sem semper erat, in consectetuer ipsum nunc id enim.'),(5,'fermentum fermentum arcu. Vestibulum'),(6,'Donec tempus, lorem fringilla ornare placerat, orci lacus vestibulum'),(7,'laoreet ipsum. Curabitur consequat, lectus sit amet'),(8,'eleifend. Cras sed leo. Cras vehicula aliquet libero. Integer in'),(9,'magna'),(10,'ac arcu. Nunc mauris. Morbi non'),(11,'primis in faucibus orci'),(12,'vehicula aliquet'),(13,'lectus'),(14,'sit amet luctus vulputate, nisi sem semper erat, in consectetuer'),(15,'semper pretium neque. Morbi quis urna.'),(16,'dui, nec tempus mauris erat eget ipsum. Suspendisse sagittis.'),(17,'orci, consectetuer euismod est arcu ac'),(18,'per conubia nostra, per inceptos hymenaeos. Mauris ut'),(19,'aliquet, metus urna'),(20,'egestas a, dui. Cras pellentesque. Sed dictum. Proin eget'),(21,'dictum eleifend, nunc risus varius orci,'),(22,'ligula. Aliquam erat volutpat. Nulla dignissim. Maecenas'),(23,'egestas'),(24,'consectetuer euismod'),(25,'malesuada fames ac turpis egestas. Aliquam fringilla cursus purus. Nullam'),(26,'semper, dui lectus rutrum urna,'),(27,'posuere cubilia Curae; Donec tincidunt. Donec vitae'),(28,'enim, condimentum eget, volutpat ornare, facilisis eget, ipsum.'),(29,'arcu ac orci. Ut semper pretium neque. Morbi'),(30,'taciti sociosqu ad litora torquent per conubia nostra,'),(31,'morbi tristique senectus et netus et malesuada fames ac'),(32,'tristique ac, eleifend vitae, erat.'),(33,'vel quam dignissim'),(34,'Cum sociis natoque'),(35,'magna. Nam ligula elit, pretium et,'),(36,'nunc.'),(37,'Phasellus libero'),(38,'at, libero. Morbi accumsan laoreet ipsum. Curabitur consequat, lectus sit'),(39,'augue. Sed molestie. Sed id risus quis diam'),(40,'Cras dolor'),(41,'Cum sociis natoque penatibus et magnis dis'),(42,'torquent per conubia'),(43,'laoreet ipsum. Curabitur consequat, lectus sit amet luctus vulputate,'),(44,'facilisi. Sed neque. Sed eget lacus. Mauris non dui nec'),(45,'Quisque ornare tortor at risus. Nunc ac'),(46,'purus gravida sagittis. Duis gravida.'),(47,'quam a felis ullamcorper viverra. Maecenas iaculis aliquet'),(48,'sed,'),(49,'velit eu sem. Pellentesque ut ipsum ac mi eleifend egestas.'),(50,'Sed neque. Sed eget lacus.');
/*!40000 ALTER TABLE `Action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Device`
--

DROP TABLE IF EXISTS `Device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Device` (
  `DeviceID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Description` varchar(150) NOT NULL,
  `Type` varchar(10) NOT NULL,
  `Manufacturer` varchar(45) DEFAULT NULL,
  `Cost` float DEFAULT NULL,
  `Unit` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`DeviceID`),
  UNIQUE KEY `name_idx` (`Name`),
  KEY `type_idx` (`Type`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device`
--

LOCK TABLES `Device` WRITE;
/*!40000 ALTER TABLE `Device` DISABLE KEYS */;
INSERT INTO `Device` VALUES (1,'Preston Horton','ullamcorper magna. Sed eu eros. Nam consequat dolor vitae','0','Diam Lorem Auctor Foundation',46,'congue.'),(2,'Baxter Warner','quam a felis ullamcorper viverra. Maecenas','1','Felis Purus Ac Industries',27,'urna.'),(3,'Christopher Gallagher','massa. Suspendisse eleifend. Cras','1','Rutrum Urna Nec Consulting',36,'elit,'),(4,'Rahim Carter','nisi','1','Sapien Corp.',10,'mi'),(5,'Hu Fields','sed, sapien. Nunc pulvinar arcu et pede. Nunc sed','1','Scelerisque Limited',2,'a,'),(6,'Ian Green','laoreet posuere, enim nisl elementum purus, accumsan interdum libero dui','1','Dictum Phasellus Institute',10,'gravida'),(7,'Garrison Blair','sem, vitae aliquam eros turpis non','1','Lobortis Risus Inc.',14,'aliquet.'),(8,'Chaim Rocha','ultrices, mauris ipsum porta elit, a feugiat tellus','0','Magna LLP',15,'Phasellus'),(9,'Kevin Graham','ante','1','Nunc In Industries',8,'malesuada'),(10,'Hakeem Webster','arcu. Sed eu nibh vulputate mauris sagittis placerat. Cras dictum','0','Consectetuer Ipsum Corporation',28,'semper'),(11,'Kane Edwards','Donec dignissim magna a tortor. Nunc commodo auctor','1','Lobortis Ltd',1,'ligula.'),(12,'Harrison Pennington','lacus.','1','Eu Corporation',9,'dignissim'),(13,'Preston Floyd','primis in faucibus','0','Felis LLC',31,'elit,'),(14,'Carlos Hampton','non enim. Mauris quis turpis vitae purus gravida','1','At Risus Nunc Consulting',20,'dignissim.'),(15,'Macaulay Atkinson','Phasellus elit pede, malesuada vel, venenatis vel, faucibus','0','Pharetra Nibh Company',35,'Nam'),(16,'Plato Douglas','enim. Sed nulla ante, iaculis nec,','1','Montes Nascetur Foundation',9,'orci'),(17,'Bert Martin','faucibus id, libero. Donec consectetuer mauris','1','Quisque Tincidunt Pede Inc.',16,'amet'),(18,'Amir Gates','risus','0','Sodales Mauris Foundation',21,'nunc'),(19,'Anthony Mitchell','lobortis tellus justo sit amet nulla.','0','Ultrices A Corporation',27,'justo.'),(20,'Castor Bass','diam luctus','0','Vitae Erat Company',16,'nec'),(21,'Ashton Yang','eros nec tellus. Nunc lectus pede, ultrices a, auctor','1','Proin Sed Limited',16,'rutrum'),(22,'Geoffrey Page','ultricies ornare, elit elit fermentum risus, at','0','Ante Ipsum LLC',8,'sem'),(23,'Merrill Blankenship','amet','0','Mauris PC',29,'massa.'),(24,'Murphy Alvarado','feugiat placerat velit. Quisque varius. Nam porttitor scelerisque','0','Cras PC',22,'consequat'),(25,'Plato Alford','magna. Ut tincidunt orci quis lectus.','0','Nibh Limited',16,'nibh.'),(26,'Abdul Matthews','risus quis diam luctus lobortis. Class aptent taciti sociosqu','0','Consectetuer Rhoncus Nullam Incorporated',18,'Nam'),(27,'Charles Cantrell','massa','1','Egestas LLC',43,'ornare.'),(28,'Connor Porter','lacus. Quisque purus sapien, gravida','0','Maecenas Iaculis Ltd',15,'sagittis'),(29,'Joshua Cote','id ante','0','Elit Dictum Eu Foundation',6,'velit'),(30,'Darius Lawson','a nunc. In at pede. Cras vulputate velit','1','Nunc LLP',29,'consequat'),(31,'Rogan Osborn','Cras sed leo. Cras vehicula aliquet libero. Integer in','1','Vulputate LLP',43,'Cras'),(32,'Brady Montgomery','dolor quam, elementum at, egestas a, scelerisque sed, sapien. Nunc','1','Gravida Non PC',43,'sem.'),(33,'Ira Snyder','montes,','0','Consequat Dolor Vitae PC',22,'magnis'),(34,'Tyler Craig','accumsan neque et nunc. Quisque ornare tortor at','0','Ligula Tortor Corp.',50,'nulla'),(35,'Otto Cash','et libero. Proin mi.','0','A Corporation',8,'dui.'),(36,'Malcolm Padilla','egestas ligula. Nullam feugiat placerat velit.','0','Lacus Pede Sagittis Institute',7,'at'),(37,'Nero Francis','Duis risus odio, auctor vitae,','1','Nec Company',49,'arcu'),(38,'Dennis Buck','varius ultrices, mauris ipsum porta elit, a','1','A LLP',42,'sit'),(39,'Isaac Rose','neque vitae semper egestas, urna','1','Ullamcorper LLP',29,'Mauris'),(40,'Duncan Paul','dui, in sodales elit erat vitae risus.','1','Hendrerit Foundation',19,'et,'),(41,'Carter Edwards','consectetuer','1','Eu Company',18,'ut'),(42,'Marshall Diaz','velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod','1','Ut Tincidunt Corp.',20,'dictum'),(43,'Rajah Britt','nunc sit amet metus. Aliquam','0','Nunc Ac Inc.',10,'Proin'),(44,'Guy Vargas','enim, condimentum eget,','1','Egestas Ligula Associates',38,'dui.'),(45,'Brendan Knight','at, egestas a, scelerisque sed, sapien. Nunc pulvinar arcu et','0','Velit Quisque Incorporated',45,'cursus'),(46,'Dennis Roberson','nibh lacinia orci, consectetuer euismod est','0','Diam Pellentesque Habitant Company',3,'vulputate'),(47,'Vaughan Farley','eros turpis non enim. Mauris quis turpis vitae purus gravida','0','Rutrum Consulting',32,'nibh'),(48,'Dennis Cook','id','1','Lorem Sit Amet Company',16,'enim'),(49,'Kaseem Carlson','malesuada fames ac turpis egestas. Fusce aliquet magna a neque.','1','Dis Associates',44,'ipsum'),(50,'Robert Willis','Vivamus rhoncus. Donec est. Nunc ullamcorper, velit in','1','Dolor Dapibus Gravida Corporation',2,'et,');
/*!40000 ALTER TABLE `Device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `History`
--

DROP TABLE IF EXISTS `History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `History` (
  `HistoryID` int NOT NULL AUTO_INCREMENT,
  `DeviceID` int NOT NULL,
  `ActionID` int NOT NULL,
  `Date` datetime NOT NULL,
  `Value` float DEFAULT NULL,
  `Comment` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`HistoryID`),
  KEY `fk_history_action1_idx` (`ActionID`),
  KEY `fk_history_device1_idx` (`DeviceID`),
  KEY `date_idx` (`Date`),
  CONSTRAINT `fk_history_action1` FOREIGN KEY (`ActionID`) REFERENCES `Action` (`ActionID`),
  CONSTRAINT `fk_history_device1` FOREIGN KEY (`DeviceID`) REFERENCES `Device` (`DeviceID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `History`
--

LOCK TABLES `History` WRITE;
/*!40000 ALTER TABLE `History` DISABLE KEYS */;
INSERT INTO `History` VALUES (1,28,25,'2021-03-15 05:14:21',7,'et magnis dis parturient montes, nascetur ridiculus'),(2,27,4,'2021-12-28 20:20:14',118,'quis massa. Mauris'),(3,26,40,'2020-07-09 04:37:35',79,'In ornare sagittis felis. Donec tempor, est ac mattis'),(4,29,16,'2022-04-07 06:35:18',172,'aliquet vel, vulputate eu, odio.'),(5,46,41,'2021-05-18 03:29:09',141,'dignissim pharetra. Nam ac nulla. In tincidunt congue turpis. In'),(6,30,43,'2022-04-04 07:33:08',85,'sed turpis nec mauris'),(7,21,16,'2022-05-03 06:16:36',174,'dui quis accumsan convallis, ante lectus convallis est, vitae sodales'),(8,5,47,'2020-11-30 10:43:57',63,'convallis dolor. Quisque tincidunt pede ac urna. Ut tincidunt vehicula'),(9,18,32,'2022-01-07 19:29:14',163,'Donec consectetuer mauris id sapien. Cras'),(10,34,35,'2021-08-19 00:02:19',198,'auctor'),(11,13,45,'2021-05-17 05:25:20',144,'Nam'),(12,24,1,'2020-08-28 20:19:57',14,'arcu. Vestibulum ut eros non enim'),(13,44,4,'2022-01-12 23:48:33',100,'rhoncus. Donec est. Nunc ullamcorper, velit'),(14,42,11,'2021-03-03 00:16:07',84,'tellus. Phasellus elit pede,'),(15,39,45,'2021-03-15 05:43:53',86,'Nam ac nulla. In tincidunt congue'),(16,8,32,'2021-01-01 02:09:49',60,'ut ipsum ac mi eleifend egestas. Sed pharetra, felis eget'),(17,49,17,'2021-10-28 13:28:53',89,'velit. Quisque varius. Nam'),(18,50,14,'2021-10-23 09:38:49',93,'lectus'),(19,22,23,'2021-03-17 02:20:37',49,'a, dui.'),(20,44,47,'2021-06-30 21:29:13',45,'molestie tellus.'),(21,25,29,'2021-07-23 11:48:46',199,'Maecenas malesuada fringilla est.'),(22,37,11,'2020-06-07 02:10:40',4,'quis diam luctus lobortis. Class aptent'),(23,22,29,'2022-02-20 01:44:24',65,'sit'),(24,36,39,'2021-12-06 20:03:51',83,'libero. Proin mi. Aliquam gravida mauris ut mi. Duis'),(25,37,10,'2020-06-24 08:21:06',41,'ornare egestas ligula.'),(26,34,8,'2020-12-16 00:10:30',88,'mollis nec, cursus a, enim. Suspendisse aliquet, sem'),(27,49,34,'2021-08-22 08:56:52',91,'feugiat. Sed nec metus facilisis lorem tristique'),(28,31,23,'2020-11-24 07:43:33',149,'Cras interdum. Nunc'),(29,38,41,'2021-03-15 19:13:37',168,'tortor at risus. Nunc ac sem ut'),(30,17,27,'2021-06-25 03:12:30',134,'vel arcu eu odio tristique pharetra. Quisque ac libero'),(31,17,1,'2020-09-13 08:54:01',89,'erat nonummy ultricies ornare, elit elit fermentum'),(32,28,24,'2021-06-21 10:47:42',22,'eu, accumsan sed, facilisis vitae, orci. Phasellus dapibus quam quis'),(33,40,29,'2021-09-29 03:55:48',76,'id risus quis diam'),(34,12,37,'2021-11-21 20:55:22',27,'leo. Vivamus nibh dolor, nonummy ac, feugiat non,'),(35,27,16,'2021-10-12 05:56:06',155,'convallis erat, eget tincidunt dui augue'),(36,6,24,'2020-10-01 21:46:28',91,'orci quis lectus. Nullam suscipit,'),(37,17,37,'2021-08-06 10:50:10',166,'non, hendrerit id,'),(38,36,33,'2020-10-29 10:14:50',92,'faucibus lectus, a'),(39,14,10,'2021-12-17 10:25:59',77,'dignissim. Maecenas ornare egestas ligula. Nullam feugiat placerat velit. Quisque'),(40,21,1,'2020-10-22 08:20:55',28,'nostra, per inceptos hymenaeos. Mauris ut quam vel'),(41,33,9,'2022-01-19 18:14:03',75,'Praesent eu nulla at sem molestie sodales. Mauris'),(42,29,43,'2021-02-20 21:52:41',69,'odio.'),(43,29,32,'2022-05-13 07:35:32',94,'arcu. Aliquam ultrices iaculis odio. Nam'),(44,29,16,'2021-09-19 16:56:09',2,'in'),(45,19,17,'2021-02-04 06:46:05',32,'vel pede blandit congue. In scelerisque scelerisque dui. Suspendisse ac'),(46,21,37,'2021-07-15 12:34:15',11,'luctus, ipsum leo elementum sem, vitae aliquam eros'),(47,48,32,'2022-05-20 18:31:05',105,'in molestie tortor nibh sit amet orci. Ut sagittis'),(48,8,2,'2021-07-26 00:57:48',62,'montes, nascetur ridiculus mus. Aenean eget magna. Suspendisse tristique'),(49,20,13,'2020-10-11 09:31:33',179,'eu lacus. Quisque imperdiet, erat nonummy ultricies ornare,'),(50,20,27,'2021-06-13 21:04:40',133,'Proin sed');
/*!40000 ALTER TABLE `History` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-25 11:54:47

-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: employee_monitoring
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `action_logs`
--

DROP TABLE IF EXISTS `action_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp_start` datetime DEFAULT NULL,
  `timestamp_end` datetime DEFAULT NULL,
  `label` varchar(255) DEFAULT NULL,
  `frames_detected` int DEFAULT NULL,
  `total_time_seconds` float DEFAULT NULL,
  `day_of_week` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action_logs`
--

LOCK TABLES `action_logs` WRITE;
/*!40000 ALTER TABLE `action_logs` DISABLE KEYS */;
INSERT INTO `action_logs` VALUES (1,'2025-04-22 11:52:28','2025-04-23 11:56:29','using_phone',405,241,'Tuesday'),(2,'2025-04-23 11:53:17','2025-04-23 11:53:52','Working',307,35,'Wednesday'),(3,'2025-04-23 11:53:52','2025-04-23 11:54:35','Drinking_Water',182,43,'Wednesday'),(4,'2025-04-23 11:54:20','2025-04-23 11:54:31','Eating',61,11,'Wednesday'),(5,'2025-04-23 11:54:28','2025-04-23 11:57:48','Arriving',273,200,'Wednesday'),(6,'2025-04-23 11:55:01','2025-04-23 11:56:22','Greeting',280,81,'Wednesday'),(7,'2025-04-23 11:55:18','2025-04-23 11:58:12','Sitting_Down',167,174,'Wednesday'),(8,'2025-04-23 11:55:23','2025-04-23 11:56:08','Conversation',405,45,'Wednesday'),(9,'2025-04-23 11:56:09','2025-04-23 11:58:22','standing_up_employee',188,133,'Wednesday'),(10,'2025-04-23 11:56:28','2025-04-23 11:59:07','Closing_Door',259,159,'Wednesday'),(11,'2025-04-23 11:56:29','2025-04-23 11:58:37','Standing',131,128,'Wednesday'),(12,'2025-04-23 11:56:39','2025-04-23 11:57:31','Sleeping',515,52,'Wednesday'),(13,'2025-04-23 11:57:41','2025-04-23 11:58:11','Idle',160,30,'Wednesday'),(14,'2025-04-23 11:58:58','2025-04-23 11:59:01','opening_door',13,3,'Wednesday'),(15,'2025-04-23 12:36:39','2025-04-23 12:40:17','opening_door',89,218,'Wednesday'),(16,'2025-04-23 12:36:44','2025-04-23 12:40:51','Closing_Door',248,247,'Wednesday'),(17,'2025-04-23 12:36:52','2025-04-23 12:41:14','Arriving',283,262,'Wednesday'),(18,'2025-04-23 12:37:08','2025-04-23 12:41:16','Standing',416,248,'Wednesday'),(19,'2025-04-23 12:37:19','2025-04-23 12:40:35','Sitting_Down',378,196,'Wednesday'),(20,'2025-04-23 12:37:24','2025-04-23 12:40:36','standing_up_employee',83,192,'Wednesday'),(21,'2025-04-23 12:37:34','2025-04-23 12:40:26','Working',320,172,'Wednesday'),(22,'2025-04-23 12:37:35','2025-04-23 12:40:35','Sleeping',108,180,'Wednesday'),(23,'2025-04-23 12:37:36','2025-04-23 12:38:40','Drinking_Water',239,64,'Wednesday'),(24,'2025-04-23 12:37:36','2025-04-23 12:40:27','Eating',628,171,'Wednesday'),(25,'2025-04-23 12:38:16','2025-04-23 12:38:39','using_phone',411,23,'Wednesday'),(26,'2025-04-23 12:39:23','2025-04-23 12:39:53','Greeting',193,30,'Wednesday'),(27,'2025-04-23 12:39:35','2025-04-23 12:39:48','Conversation',176,13,'Wednesday'),(28,'2025-04-23 12:39:57','2025-04-23 12:41:21','falling_down',159,84,'Wednesday'),(29,'2025-04-23 12:39:57','2025-04-23 12:40:28','Idle',151,31,'Wednesday'),(30,'2025-04-23 12:41:17','2025-04-23 12:41:18','Leaving',11,1,'Wednesday'),(31,'2025-04-24 09:16:30','2025-04-24 09:25:46','Arriving',157,556,'Thursday'),(32,'2025-04-24 09:16:43','2025-04-24 09:25:50','Sitting_Down',349,547,'Thursday'),(33,'2025-04-24 09:16:58','2025-04-24 09:25:16','Working',381,498,'Thursday'),(34,'2025-04-24 09:17:00','2025-04-24 09:25:14','Eating',1730,494,'Thursday'),(35,'2025-04-24 09:21:02','2025-04-24 09:25:55','Standing',224,293,'Thursday'),(36,'2025-04-24 09:21:03','2025-04-24 09:25:55','standing_up_employee',223,292,'Thursday'),(37,'2025-04-24 09:21:22','2025-04-24 09:21:48','Conversation',265,26,'Thursday'),(38,'2025-04-24 09:21:54','2025-04-24 09:22:02','Greeting',130,8,'Thursday'),(39,'2025-04-24 09:22:03','2025-04-24 09:24:35','Drinking_Water',477,152,'Thursday'),(40,'2025-04-24 09:22:03','2025-04-24 09:25:22','using_phone',746,199,'Thursday'),(41,'2025-04-24 09:22:47','2025-04-24 09:25:07','Idle',394,140,'Thursday'),(42,'2025-04-24 09:22:52','2025-04-24 09:25:24','Sneezing',360,152,'Thursday'),(43,'2025-04-24 09:22:52','2025-04-24 09:25:25','Sleeping',225,153,'Thursday'),(44,'2025-04-24 09:25:56','2025-04-24 09:26:16','falling_down',196,20,'Thursday'),(45,'2025-04-24 09:26:16','2025-04-24 09:26:30','opening_door',119,14,'Thursday'),(46,'2025-04-24 09:26:25','2025-04-24 09:26:31','Closing_Door',75,6,'Thursday'),(47,'2025-04-25 14:50:00','2025-04-25 14:50:05','opening_door',32,5,'Friday'),(48,'2025-04-25 14:50:05','2025-04-25 15:01:00','Closing_Door',130,655,'Friday'),(49,'2025-04-25 14:50:16','2025-04-25 15:00:59','Arriving',173,643,'Friday'),(50,'2025-04-25 14:50:23','2025-04-25 15:00:58','falling_down',180,635,'Friday'),(51,'2025-04-25 14:50:26','2025-04-25 15:00:54','Standing',218,628,'Friday'),(52,'2025-04-25 14:50:27','2025-04-25 15:00:27','Sitting_Down',323,600,'Friday'),(53,'2025-04-25 14:50:47','2025-04-25 14:57:05','Eating',982,378,'Friday'),(54,'2025-04-25 14:51:31','2025-04-25 14:58:58','Working',336,447,'Friday'),(55,'2025-04-25 14:52:43','2025-04-25 14:55:58','Drinking_Water',526,195,'Friday'),(56,'2025-04-25 14:54:01','2025-04-25 14:59:22','standing_up_employee',324,321,'Friday'),(57,'2025-04-25 14:54:01','2025-04-25 14:58:48','Sleeping',314,287,'Friday'),(58,'2025-04-25 14:54:03','2025-04-25 14:55:33','Greeting',170,90,'Friday'),(59,'2025-04-25 14:54:28','2025-04-25 14:55:21','Conversation',460,53,'Friday'),(60,'2025-04-25 14:56:20','2025-04-25 14:56:57','Sneezing',234,37,'Friday'),(61,'2025-04-25 14:56:36','2025-04-25 15:00:33','Idle',225,237,'Friday');
/*!40000 ALTER TABLE `action_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-27 12:43:41

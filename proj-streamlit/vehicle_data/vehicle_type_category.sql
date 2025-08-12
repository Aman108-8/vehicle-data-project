-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: vehicle
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `vehicle_type_category`
--

DROP TABLE IF EXISTS `vehicle_type_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_type_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicle_type_id` int NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vehicle_type_id` (`vehicle_type_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `vehicle_type_category_ibfk_1` FOREIGN KEY (`vehicle_type_id`) REFERENCES `vehicle` (`vehicle_id`),
  CONSTRAINT `vehicle_type_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `vehicle_category` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_type_category`
--

LOCK TABLES `vehicle_type_category` WRITE;
/*!40000 ALTER TABLE `vehicle_type_category` DISABLE KEYS */;
INSERT INTO `vehicle_type_category` VALUES (1,1,31),(2,1,32),(3,1,36),(4,1,40),(5,1,41),(6,1,42),(7,2,54),(8,2,55),(9,2,56),(10,2,19),(11,2,20),(12,3,2),(13,3,3),(14,3,5),(15,3,8),(16,3,9),(17,3,12),(18,3,13),(19,3,14),(20,3,15),(21,3,16),(22,3,17),(23,3,18),(24,3,23),(25,3,24),(26,3,25),(27,3,26),(28,3,27),(29,3,28),(30,3,29),(31,3,30),(32,3,33),(33,3,34),(34,3,35),(35,3,37),(36,3,38),(37,3,39),(38,3,43),(39,3,44),(40,3,45),(41,3,46),(42,3,47),(43,3,48),(44,3,49),(45,3,50),(46,3,51),(47,3,52),(48,3,53),(49,3,57),(50,3,58),(51,3,59),(52,3,60),(53,3,61),(54,3,62),(55,3,63),(56,3,64),(57,3,65);
/*!40000 ALTER TABLE `vehicle_type_category` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-12 16:48:50

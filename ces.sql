-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: ces
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `enquiry`
--

DROP TABLE IF EXISTS `enquiry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enquiry` (
  `enquiry_no` int NOT NULL,
  `user_id` int NOT NULL,
  `date` date NOT NULL,
  `dept_id` varchar(50) NOT NULL,
  `seat_locked` tinyint(1) NOT NULL DEFAULT '0',
  KEY `enquiry_enquiry_no_fk` (`enquiry_no`),
  KEY `enquiry_deptid_fk` (`dept_id`),
  KEY `enquiry_userid_fk_idx` (`user_id`),
  CONSTRAINT `enquiry_deptid_fk` FOREIGN KEY (`dept_id`) REFERENCES `seat_availability` (`dept_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `enquiry_enquiry_no_fk` FOREIGN KEY (`enquiry_no`) REFERENCES `userdetails` (`application_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `enquiry_userid_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enquiry`
--

LOCK TABLES `enquiry` WRITE;
/*!40000 ALTER TABLE `enquiry` DISABLE KEYS */;
INSERT INTO `enquiry` VALUES (24,14,'2024-05-10','54321',0),(25,16,'2024-05-10','54321',1);
/*!40000 ALTER TABLE `enquiry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,'hello all');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat_availability`
--

DROP TABLE IF EXISTS `seat_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat_availability` (
  `dept_id` varchar(50) NOT NULL,
  `deptname` varchar(200) NOT NULL,
  `totalseats` int NOT NULL,
  `intake` int NOT NULL,
  `freeseats` int NOT NULL,
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat_availability`
--

LOCK TABLES `seat_availability` WRITE;
/*!40000 ALTER TABLE `seat_availability` DISABLE KEYS */;
INSERT INTO `seat_availability` VALUES ('54321','csc',100,2,98);
/*!40000 ALTER TABLE `seat_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdetails`
--

DROP TABLE IF EXISTS `userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdetails` (
  `application_no` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `sname` varchar(200) NOT NULL,
  `dob` date NOT NULL,
  `fathername` varchar(200) NOT NULL,
  `mothername` varchar(200) NOT NULL,
  `schoolname` varchar(200) NOT NULL,
  `10th_board` varchar(200) NOT NULL,
  `10th_percentage` float NOT NULL,
  `12th_board` varchar(200) NOT NULL,
  `12th_percentage` float NOT NULL,
  `12th_cutoff` float NOT NULL,
  `caste` varchar(200) NOT NULL,
  `community` varchar(200) NOT NULL,
  `annual_income` int NOT NULL,
  `quota` varchar(200) NOT NULL,
  `sis_bro_studying` tinyint(1) NOT NULL DEFAULT '0',
  `sis_bro_name` varchar(200) DEFAULT NULL,
  `sis_bro_dept` varchar(200) DEFAULT NULL,
  `dept_asking_id` varchar(20) NOT NULL,
  PRIMARY KEY (`application_no`),
  KEY `userdetails_deptaskingid_fk` (`dept_asking_id`),
  KEY `userdetails_userid_fk_idx` (`user_id`),
  CONSTRAINT `userdetails_deptaskingid_fk` FOREIGN KEY (`dept_asking_id`) REFERENCES `seat_availability` (`dept_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `userdetails_userid_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdetails`
--

LOCK TABLES `userdetails` WRITE;
/*!40000 ALTER TABLE `userdetails` DISABLE KEYS */;
INSERT INTO `userdetails` VALUES (24,14,'vijayalakshmi','2002-12-04','father','mother','school','vijayas',92,'vijayas',89,50,'OBC','com',10000,'Counselling',0,NULL,NULL,'54321'),(25,16,'nagalakshmi','2024-05-11','nagu father','nagu mother','school','nagu',99,'nagu',82,50,'BC','com',100000,'Counselling',0,NULL,NULL,'54321');
/*!40000 ALTER TABLE `userdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varbinary(200) NOT NULL,
  `confirm_password` varbinary(200) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (14,'vijayalakshmi@codegnan.com',_binary '1234',_binary '1234'),(16,'nagalakshmi@codegnan.com',_binary '1234',_binary '1234');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-25 16:18:05

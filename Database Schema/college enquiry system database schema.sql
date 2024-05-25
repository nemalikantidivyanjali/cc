-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: collegeenquirysystem
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
INSERT INTO `enquiry` VALUES (18,5,'2021-10-10','D02',1),(19,11,'2021-10-10','D04',0);
/*!40000 ALTER TABLE `enquiry` ENABLE KEYS */;
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
INSERT INTO `seat_availability` VALUES ('D01','B.E Aeronautical Engineering',300,100,200),('D02','B.E Bio-Medical Engineering',200,51,149),('D03','B.Tech Bio-Technology',250,100,150),('D04','B.Tech Computer Science and Engineering',250,200,50),('D05','B.E Electronics and Communication Engineering',200,100,100);
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdetails`
--

LOCK TABLES `userdetails` WRITE;
/*!40000 ALTER TABLE `userdetails` DISABLE KEYS */;
INSERT INTO `userdetails` VALUES (18,5,'SaiCharan','2001-08-16','random','random','random','random',90,'random',89,170,'OBC','random',500000,'Management',0,NULL,NULL,'D02'),(19,11,'Surendhar','2001-12-20','random','random','random school','random board',90,'random board',90,170,'BC','random',500000,'Management',0,NULL,NULL,'D04');
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
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'suren123@gmail.com',_binary '$2b$12$i6YMmMQ524iZalkLotpULOzGEkLDwH6lA..vhlXfD96udM/JgL6lW',_binary '$2b$12$uZuBHehb9RPNH.XlZXutuOCoDP5ncqq/HnZrfZAiCR81U2MpEnd2C',0),(2,'admin@gmail.com',_binary '$2b$12$jyRHSc3/zQJhIIMMrp0uX.vyglJM83qZwIgnE6XHkPYuHw4cp7Iau',_binary '$2b$12$u6EV9P8Jl22AlPr2Zx6K/OfgKyRPhYTQFFbSGkP17JALgDKEF1hxK',1),(5,'sai123@gmail.com',_binary '$2b$12$1mZ8oh9pvw3HdZDJM/BNUOjT54h1BL3cIqXrXwber2XW8KMkvyZF2',_binary '$2b$12$cky28y.IBPKTgSMkoZAr0Ou18vrQkjH3r4CKh5revAsVlcCVfoJvG',0),(8,'surenharish007@gmail.com',_binary '$2b$12$1MSz.dIGgCmPFRoQepCoG.qjvyN9bjJnGEkicAxW4.5GRfqkc5tim',_binary '$2b$12$CwQfndG9D.lVE8O6GpXk7e5AE6ip5mNGRGkejUQtkNe0quaxYLKHC',0),(9,'ashwinprasad202@gmail.com',_binary '$2b$12$phXxtpWvLokcbVv3j1FT.OrUVAKAdG82PnfytnnvoLiq3VymMdbUi',_binary '$2b$12$GrdrrthzBZXFJPbZge0faeZYPx2qGq1Y60Z7prSWuIb017JK1tz8C',0),(10,'vijayalakshmi2k01@gmail.com',_binary '$2b$12$vmRb0b0AJqSBr4ok5AJ5LOHRhj6KOT7r3FMjnN3TxiXmxnCeF/7v2',_binary '$2b$12$tsG0GUnirrLp1rfubzXFLuYLyKZIaaLWloS.Djzjtnki2BnLGmboW',0),(11,'surendhar.r.2019.csbs@rajalakshmi.edu.in',_binary '$2b$12$ftDHewz77KhsMDUU6fF6R.vKnoLbvqrmqVBia1sr5QgmfCMNpKSq2',_binary '$2b$12$bKuuE.vaGNU34FHhTxMQyOZoFB/lBfabZl73bL5vr3ca8MjSFrzv6',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'collegeenquirysystem'
--

--
-- Dumping routines for database 'collegeenquirysystem'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-17 23:02:31

/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - messmanagement_db
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`messmanagement_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `messmanagement_db`;

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `Id` VARCHAR(10) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `feedback` varchar(100) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `food_bill` */

DROP TABLE IF EXISTS `food_bill`;

CREATE TABLE `food_bill` (
  `Id` VARCHAR(10) DEFAULT NULL ,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Food_Type` varchar(100) DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `Month` varchar(100) DEFAULT NULL,
  `Year` varchar(100) DEFAULT NULL,
  `Time` varchar(100) DEFAULT NULL,
  `Amount` int(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `Id` VARCHAR(10) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `CardName` varchar(100) DEFAULT NULL,
  `CardNo` varchar(100) DEFAULT NULL,
  `CVV` varchar(100) DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `Payed_date` varchar(100) DEFAULT NULL,
  `Amount` varchar(100) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `userinfo` */

DROP TABLE IF EXISTS `userinfo`;

CREATE TABLE `userinfo` (
  `Id` VARCHAR(10) DEFAULT NULL,
  `Name` varchar(200) DEFAULT NULL,
  `Email` varchar(200) DEFAULT NULL,
  `Contact` varchar(200) DEFAULT NULL,
  `Password` varchar(200) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  `train_status` varchar(100) DEFAULT 'pending'
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;



/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`dse_configcenter` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `dse_configcenter`;

/*Table structure for table `businessconfig` */

DROP TABLE IF EXISTS `businessconfig`;

CREATE TABLE `businessconfig` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `identifier` varchar(100) DEFAULT NULL,
  `sendeType` char(50) DEFAULT NULL,
  `configtype` varchar(50) DEFAULT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `encryptType` tinyint(3) DEFAULT NULL,
  `encryKeyPub` varchar(400) DEFAULT NULL,
  `encryKeyPri` varchar(400) DEFAULT NULL,
  `createTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


/*Table structure for table `systemconfig` */

DROP TABLE IF EXISTS `systemconfig`;

CREATE TABLE `systemconfig` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL COMMENT '配置类型',
  `key` varchar(100) DEFAULT NULL COMMENT '配置key',
  `confjsonStr` varchar(200) DEFAULT NULL COMMENT '配置json串',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;



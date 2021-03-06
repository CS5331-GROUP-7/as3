-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 23, 2018 at 03:37 PM
-- Server version: 5.5.41-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cs5331`
--
CREATE DATABASE IF NOT EXISTS `cs5331` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `cs5331`;

-- --------------------------------------------------------

--
-- Table structure for table `example`
--

DROP TABLE IF EXISTS `example`;
CREATE TABLE IF NOT EXISTS `example` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `example`
--

INSERT INTO `example` (`id`, `title`, `content`, `Timestamp`) VALUES
(1, 'hello world', 'welcome to my guestbook', '2015-02-08 01:06:27');

-- --------------------------------------------------------

--
-- Table structure for table `table13`
--

DROP TABLE IF EXISTS `table13`;
CREATE TABLE IF NOT EXISTS `table13` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `table13`
--

INSERT INTO `table13` (`id`, `title`, `content`, `Timestamp`) VALUES
(1, 'hello world', 'welcome to my guestbook', '2015-02-08 01:06:27');

-- --------------------------------------------------------

--
-- Table structure for table `table17`
--

DROP TABLE IF EXISTS `table17`;
CREATE TABLE IF NOT EXISTS `table17` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` char(128) NOT NULL,
  `salt` char(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `table17`
--

INSERT INTO `table17` (`id`, `username`, `email`, `password`, `salt`) VALUES
(1, 'admin', 'admin@admin.com', 'a6ab787fdace563008c45f14aa9d5da5e3c0ef41acfe76ec09212484ba641ee9fc228db69104d207ff32e4cdfd294be1300921143531977661bce7daef3b6433', '9614ba56553bd6a5707831ebed9395de81096571cbd1282b97a5755c21464072f4e890030ebd5111aef9e7cda18d4e75c503b28e0860d35e9bc3a45adc89e7dc');

-- --------------------------------------------------------

--
-- Table structure for table `table19`
--

DROP TABLE IF EXISTS `table19`;
CREATE TABLE IF NOT EXISTS `table19` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `table19`
--

INSERT INTO `table19` (`id`, `title`, `content`, `Timestamp`) VALUES
(1, 'hello world', 'welcome to my guestbook', '2015-02-08 01:06:27'),
(2, '<script>alert(document.cookie)</script>', 'fsd', '2015-02-16 19:30:46');

-- --------------------------------------------------------

--
-- Table structure for table `table20`
--

DROP TABLE IF EXISTS `table20`;
CREATE TABLE IF NOT EXISTS `table20` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` char(128) NOT NULL,
  `salt` char(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `table20`
--

INSERT INTO `table20` (`id`, `username`, `email`, `password`, `salt`) VALUES
(1, 'admin', 'admin@admin.com', '6yEJedUJsxsQY2s', 'no salt');

-- --------------------------------------------------------

--
-- Table structure for table `table22`
--

DROP TABLE IF EXISTS `table22`;
CREATE TABLE IF NOT EXISTS `table22` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `voucher` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`user`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1247473648 ;

--
-- Dumping data for table `table22`
--

INSERT INTO `table22` (`id`, `user`, `password`, `voucher`) VALUES
(1, 'normal', '5f4dcc3b5aa765d61d8327deb882cf99', ''),
(1247473647, 'admin', 'impossibletogetinusingpassword', 'upcYmp7DWrwXF9k');

-- --------------------------------------------------------

--
-- Table structure for table `table23`
--

DROP TABLE IF EXISTS `table23`;
CREATE TABLE IF NOT EXISTS `table23` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` char(128) NOT NULL,
  `salt` char(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `table23`
--

INSERT INTO `table23` (`id`, `username`, `email`, `password`, `salt`) VALUES
(1, 'a', 'a@a.com', '4f2f395c5c307f328a88c7f138e9cc50d5c8294fcdc3e005b47831cacd83fc2b019401baf0a58437073f4e92ffde0a2433534ee49880e6df5f1a254a10f70546', '6620b990250a816c6192b486e6eebdc18eee0e455fcc30366a9667592802bf296bc423b6bcc12bf2752b748e12613a5341decbc362ec28bffc251bbb39581cab');

-- --------------------------------------------------------

--
-- Table structure for table `table24`
--

DROP TABLE IF EXISTS `table24`;
CREATE TABLE IF NOT EXISTS `table24` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `table24`
--

INSERT INTO `table24` (`id`, `first_name`, `last_name`, `timestamp`) VALUES
(-1532558121, 'admin', 'flag is W5JAU77cnaRSNQP', '2015-02-10 06:21:03'),
(1, 'John', 'Davidson', '2015-02-10 05:50:41'),
(2, 'Peter', 'Jack', '2015-02-10 05:51:00'),
(3, 'Mary', 'Jane', '2015-02-10 05:51:17');

-- --------------------------------------------------------

--
-- Table structure for table `table4`
--

DROP TABLE IF EXISTS `table4`;
CREATE TABLE IF NOT EXISTS `table4` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` varchar(5000) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `table4`
--

INSERT INTO `table4` (`id`, `title`, `content`, `Timestamp`) VALUES
(1, 'hello world', 'welcome to my guestbook', '2015-02-08 01:06:27');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

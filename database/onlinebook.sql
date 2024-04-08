-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:4306
-- Generation Time: Feb 23, 2024 at 09:01 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `menshut`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `confirmCode` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `firstName`, `lastName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(6, 'ashish', 'adhikari', 'acaashish08@gmail.com', '9813672338', 'ktm', '$5$rounds=535000$FhMk2cK7aQkbTmK/$iniAviA1gIjPJuJ28Y2BgfeFs08ZbK5ylTOLYEABx97', 'owner', '0');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `uid` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`uid`, `pid`, `quantity`) VALUES
(17, 8, 1),
(17, 8, 1),
(17, 1, 1),
(17, 2, 1),
(17, 5, 2),
(17, 6, 1),
(17, 20, 1),
(NULL, 6, 1),
(16, 8, 1),
(NULL, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `ofname` text NOT NULL,
  `pid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `oplace` text NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `dstatus` varchar(10) NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT current_timestamp(),
  `ddate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `uid`, `ofname`, `pid`, `quantity`, `oplace`, `mobile`, `dstatus`, `odate`, `ddate`) VALUES
(14, 16, 'family family', 9, 2, 'ktm', '9813672338', 'no', '2024-02-23 07:49:45', '2024-03-01'),
(15, 16, 'the house of last resort ', 5, 1, 'ktm', '9813672338', 'no', '2024-02-23 07:52:49', '2024-03-01');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `pid` int(11) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(70) DEFAULT NULL,
  `image` varchar(255) NOT NULL,
  `category` varchar(70) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `discount` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`pid`, `code`, `name`, `image`, `category`, `price`, `discount`) VALUES
(3, 'EDNALAN01', 'Samsung Galaxy A10S', '2.jpg', 'Mobile', 520, 100),
(4, 'EDNALAN02', 'Samsung Galaxy Win Duos', '3.jpg', 'Mobile', 1600, 500),
(5, 'EDNALAN03', 'Women Summer Spaghetti Strap Down', '4.jpg', 'Woman Dresess', 2020, 1250),
(6, 'EDNALAN04', 'Honda TMX Alpha Clamp', '5.jpg', 'Motorcycle', 320, 50);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `pName` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `available` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `item` varchar(100) NOT NULL,
  `pCode` varchar(20) NOT NULL,
  `picture` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `pName`, `price`, `author`, `available`, `category`, `item`, `pCode`, `picture`, `date`, `status`) VALUES
(1, 'The chimp paradox', 120, 'book  by Prof Steve Peters', 4, 'fiction', 'book', 't-007', 'thechimpparadox.jpg', '2018-09-20 07:10:40', '20% off'),
(2, 'Salt: A World History', 600, 'book by Mark Kurlansky', 3, 'nonfiction', 'book', 'w-004', 'salt.jpg', '2024-02-17 12:01:36', NULL),
(3, '1776', 200, 'book by David McCullough\r\n', 8, 'history', 'book', '#-001', '1776.jpg', '2024-02-16 18:15:00', NULL),
(4, '1984', 1200, 'book by George Orwell,\r\nThomas Pynchon\r\n (Foreword)', 9, 'scifi', 'book', 'b-001', '1984.jpg', '2024-02-16 18:15:00', NULL),
(5, 'The House of last Resort', 500, ' book by Christopher Golden', 10, 'fiction', 'book', 's-002', 'thehouseoflastresort.jpg', '2018-09-20 08:40:06', NULL),
(6, 'Rabbit Hole', 300, 'book by Kate brody', 12, 'fiction', 'book', 't-003', 'rabbithole.jpg', '2018-09-20 08:41:18', NULL),
(7, 'The Busy Body', 200, ' book by Kemper Donovan', 10, 'fiction', 'book', 't-004', 'thebusybody.jpg', '2018-09-20 08:42:11', NULL),
(8, 'Womb City', 200, 'book by Tlotlo Tsamaase', 20, 'fiction', 'book', 't-005', 'wombcity.png', '2018-09-20 08:45:39', NULL),
(9, 'Family Family', 500, 'book by Laurie Frankel\r\n', 20, 'fiction', 'book', 't-006', 'familyfamily.png', '2018-09-20 08:57:07', NULL),
(10, 'This Wretched Valley', 1000, 'book by Jenny Kiefer', 5, 'fiction', 'book', 't-007', 'thewretchedvalley.png', '2018-09-20 08:58:38', NULL),
(12, 'Where You End', 300, 'book by Abbott Kahler', 10, 'fiction', 'book', 't-010', 'whereyouend.jpg', '2018-09-20 09:02:04', NULL),
(13, 'John Adams', 200, 'book by David McCullough', 10, 'history', 'book', 's-002', 'johna.jpg', '2024-02-16 18:15:00', NULL),
(14, 'Brave New World', 200, 'book by Aldous Huxley', 20, 'scifi', 'book', 'b-003', 'BNW.jpg', '2024-02-16 18:15:00', NULL),
(15, 'Ender’s Game', 300, 'book by Orson Scott Card', 20, 'scifi', 'book', 'b-004', 'EG.jpg', '2024-02-16 18:15:00', NULL),
(16, 'Dune', 300, 'book by Frank Herbert', 15, 'scifi', 'book', 'b-005', 'dune.jpg', '2024-02-16 18:15:00', NULL),
(17, 'Stiff: The Curious Lives of Human Cadavers', 100, 'book by Mary Roach', 10, 'nonfiction', 'book', 'w-005', 'stiff.jpg', '2018-10-01 03:51:52', NULL),
(19, 'Fight Right', 300, 'book by Julie Schwartz Gottman,\r\nJohn M. Gottman', 20, 'nonfiction', 'book', 'w-009', 'fightright.jpg', '2018-10-01 03:53:37', NULL),
(20, 'The Rise and Fall of the Third Reich: A History of Nazi Germany\r\n\r\n', 1200, 'book by William L. Shirer', 23, 'history', 'book', 's-003', 'THE.jpg', '2024-02-16 18:15:00', NULL),
(21, 'The Guns of August', 200, 'book by Barbara W. Tuchman', 12, 'history', 'book', 's-004', 'thegun.jpg', '2024-02-17 14:57:46', NULL),
(22, 'The joy of PHP\r\n', 200, 'book', 10, 'nonfiction', 'book', '#08', 'joy-php.jpg', '2024-02-10 06:14:01', NULL),
(23, 'fluke', 100, 'book by Brian Klaas', 10, 'nonfiction', 'book', 'w-006', 'fluke.jpg', '2018-10-01 03:51:52', NULL),
(24, 'First Things First', 100, 'book by Nadirah Simmons', 10, 'nonfiction', 'book', 'w-006', 'FTF.jpg', '2024-02-16 18:15:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `product_level`
--

CREATE TABLE `product_level` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `v_shape` varchar(10) NOT NULL DEFAULT 'no',
  `polo` varchar(10) NOT NULL DEFAULT 'no',
  `clean_text` varchar(10) NOT NULL DEFAULT 'no',
  `design` varchar(10) NOT NULL DEFAULT 'no',
  `chain` varchar(10) NOT NULL DEFAULT 'no',
  `leather` varchar(10) NOT NULL DEFAULT 'no',
  `hook` varchar(10) NOT NULL DEFAULT 'no',
  `color` varchar(10) NOT NULL DEFAULT 'no',
  `formal` varchar(10) NOT NULL DEFAULT 'no',
  `converse` varchar(10) NOT NULL DEFAULT 'no',
  `loafer` varchar(10) NOT NULL DEFAULT 'no'
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `product_level`
--

INSERT INTO `product_level` (`id`, `product_id`, `v_shape`, `polo`, `clean_text`, `design`, `chain`, `leather`, `hook`, `color`, `formal`, `converse`, `loafer`) VALUES
(1, 1, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(2, 2, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(3, 3, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(4, 4, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(5, 5, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(6, 6, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(7, 7, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(9, 9, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(10, 10, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(14, 14, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(12, 12, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(13, 13, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(15, 15, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no'),
(16, 16, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no'),
(17, 17, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(18, 18, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(19, 19, 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(20, 20, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'),
(21, 21, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no'),
(22, 22, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `product_view`
--

CREATE TABLE `product_view` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `product_view`
--

INSERT INTO `product_view` (`id`, `user_id`, `product_id`, `date`) VALUES
(1, 9, 9, '2018-09-22 02:19:30'),
(2, 9, 7, '2018-09-27 02:47:43'),
(3, 9, 12, '2018-09-22 03:20:59'),
(4, 9, 10, '2018-09-29 03:07:11'),
(5, 9, 5, '2018-09-22 03:19:19'),
(6, 9, 8, '2018-09-21 15:57:50'),
(7, 9, 6, '2018-09-22 02:12:54'),
(8, 9, 1, '2018-09-22 03:03:36'),
(9, 16, 5, '2024-02-19 10:57:09'),
(10, 16, 7, '2024-02-22 14:16:56'),
(11, 16, 22, '2024-02-11 14:22:25'),
(12, 16, 1, '2024-02-22 14:15:38'),
(13, 16, 8, '2024-02-20 11:09:07'),
(14, 16, 6, '2024-02-18 13:14:55'),
(15, 16, 10, '2024-02-17 11:27:16'),
(16, 17, 1, '2024-02-22 16:41:39'),
(17, 17, 8, '2024-02-22 16:41:31'),
(18, 17, 12, '2024-02-22 16:38:55'),
(19, 17, 6, '2024-02-22 16:33:19'),
(20, 17, 5, '2024-02-22 16:56:37'),
(21, 17, 7, '2024-02-22 16:38:19'),
(22, 17, 10, '2024-02-22 16:52:13'),
(23, 17, 9, '2024-02-22 16:35:07'),
(24, 17, 8, '2024-02-22 16:58:49'),
(25, 17, 5, '2024-02-22 16:59:15'),
(26, 17, 1, '2024-02-22 17:00:18'),
(27, 17, 7, '2024-02-22 17:01:40'),
(28, 17, 1, '2024-02-22 17:01:42'),
(29, 17, 5, '2024-02-22 17:01:46'),
(30, 17, 1, '2024-02-22 17:02:01'),
(31, 17, 10, '2024-02-22 17:02:25'),
(32, 17, 5, '2024-02-22 17:02:30'),
(33, 17, 7, '2024-02-22 17:02:34'),
(34, 17, 5, '2024-02-22 17:05:03'),
(35, 17, 5, '2024-02-22 17:05:08'),
(36, 17, 8, '2024-02-22 17:05:25'),
(37, 17, 5, '2024-02-22 17:05:30'),
(38, 17, 1, '2024-02-22 17:06:04'),
(39, 17, 1, '2024-02-22 17:06:41'),
(40, 17, 1, '2024-02-22 17:07:01'),
(41, 17, 7, '2024-02-22 17:07:31'),
(42, 17, 7, '2024-02-22 17:08:38'),
(43, 17, 8, '2024-02-22 17:09:14'),
(44, 17, 12, '2024-02-22 17:09:44'),
(45, 17, 6, '2024-02-22 17:10:00'),
(46, 17, 1, '2024-02-22 17:10:05'),
(47, 17, 9, '2024-02-22 17:10:20'),
(48, 17, 9, '2024-02-22 17:11:05'),
(49, 17, 12, '2024-02-22 17:12:36'),
(50, 17, 12, '2024-02-22 17:12:40'),
(51, 17, 8, '2024-02-22 17:13:12'),
(52, 17, 1, '2024-02-22 17:16:34'),
(53, 17, 1, '2024-02-22 17:16:38'),
(54, 17, 12, '2024-02-22 17:17:00'),
(55, 17, 5, '2024-02-22 17:17:08'),
(56, 17, 5, '2024-02-22 17:18:08'),
(57, 17, 5, '2024-02-22 17:18:33'),
(58, 17, 1, '2024-02-22 17:18:36'),
(59, 17, 12, '2024-02-22 17:22:02'),
(60, 17, 12, '2024-02-22 17:24:01'),
(61, 17, 8, '2024-02-22 17:24:40'),
(62, 17, 5, '2024-02-22 17:29:04'),
(63, 17, 7, '2024-02-22 17:31:02'),
(64, 17, 9, '2024-02-22 17:31:22'),
(65, 17, 10, '2024-02-22 17:32:28'),
(66, 17, 7, '2024-02-22 17:32:49'),
(67, 17, 10, '2024-02-22 17:33:35'),
(68, 17, 12, '2024-02-22 17:34:23'),
(69, 17, 7, '2024-02-22 17:34:34'),
(70, 17, 12, '2024-02-22 17:35:54'),
(71, 17, 1, '2024-02-22 17:40:02'),
(72, 17, 6, '2024-02-22 17:46:25'),
(73, 17, 1, '2024-02-23 04:13:43'),
(74, 17, 9, '2024-02-23 04:13:52'),
(75, 17, 5, '2024-02-23 04:13:59'),
(76, 17, 7, '2024-02-23 04:21:51'),
(77, 17, 1, '2024-02-23 04:30:08'),
(78, 17, 7, '2024-02-23 04:30:17'),
(79, 17, 7, '2024-02-23 04:32:22'),
(80, 17, 1, '2024-02-23 04:32:34'),
(81, 17, 1, '2024-02-23 04:33:04'),
(82, 17, 1, '2024-02-23 04:39:13'),
(83, 17, 5, '2024-02-23 04:39:16'),
(84, 17, 6, '2024-02-23 04:39:19'),
(85, 17, 7, '2024-02-23 04:39:23'),
(86, 17, 1, '2024-02-23 04:40:16'),
(87, 17, 1, '2024-02-23 04:40:46'),
(88, 17, 1, '2024-02-23 04:41:23'),
(89, 17, 1, '2024-02-23 04:41:27'),
(90, 17, 1, '2024-02-23 04:41:44'),
(91, 17, 1, '2024-02-23 04:41:45'),
(92, 17, 1, '2024-02-23 04:42:06'),
(93, 17, 9, '2024-02-23 04:49:34'),
(94, 17, 1, '2024-02-23 04:54:16'),
(95, 17, 12, '2024-02-23 04:57:14'),
(96, 17, 10, '2024-02-23 04:59:55'),
(97, 17, 8, '2024-02-23 05:12:08'),
(98, 17, 1, '2024-02-23 05:21:10'),
(99, 17, 7, '2024-02-23 05:21:20'),
(100, 17, 12, '2024-02-23 05:21:32'),
(101, 17, 9, '2024-02-23 05:21:39'),
(102, 17, 9, '2024-02-23 05:22:00'),
(103, 17, 8, '2024-02-23 05:22:02'),
(104, 17, 8, '2024-02-23 05:22:13'),
(105, 17, 1, '2024-02-23 05:22:19'),
(106, 17, 5, '2024-02-23 05:22:25'),
(107, 17, 1, '2024-02-23 05:22:35'),
(108, 17, 6, '2024-02-23 05:22:46'),
(109, 17, 5, '2024-02-23 05:22:51'),
(110, 17, 1, '2024-02-23 05:22:56'),
(111, 17, 1, '2024-02-23 05:24:13'),
(112, 17, 5, '2024-02-23 05:24:22'),
(113, 17, 1, '2024-02-23 05:38:35'),
(114, 17, 1, '2024-02-23 05:44:42'),
(115, 16, 5, '2024-02-23 05:45:44'),
(116, 16, 6, '2024-02-23 05:49:41'),
(117, 16, 6, '2024-02-23 05:49:49'),
(118, 16, 10, '2024-02-23 05:52:20'),
(119, 16, 1, '2024-02-23 06:01:24'),
(120, 16, 8, '2024-02-23 06:23:13'),
(121, 16, 7, '2024-02-23 06:23:22'),
(122, 16, 7, '2024-02-23 06:23:46'),
(123, 16, 7, '2024-02-23 06:53:48'),
(124, 16, 5, '2024-02-23 07:06:55'),
(125, 16, 8, '2024-02-23 07:07:50'),
(126, 16, 10, '2024-02-23 07:09:08'),
(127, 16, 6, '2024-02-23 07:12:09'),
(128, 16, 1, '2024-02-23 07:13:30'),
(129, 16, 6, '2024-02-23 07:17:38'),
(130, 16, 1, '2024-02-23 07:30:06'),
(131, 16, 1, '2024-02-23 07:30:18'),
(132, 16, 1, '2024-02-23 07:30:28'),
(133, 16, 6, '2024-02-23 07:30:33'),
(134, 16, 7, '2024-02-23 07:30:49'),
(135, 16, 1, '2024-02-23 07:32:30'),
(136, 16, 6, '2024-02-23 07:33:23'),
(137, 16, 8, '2024-02-23 07:35:13'),
(138, 16, 8, '2024-02-23 07:36:09'),
(139, 16, 8, '2024-02-23 07:40:01'),
(140, 16, 6, '2024-02-23 07:40:11'),
(141, 16, 10, '2024-02-23 07:40:18'),
(142, 16, 1, '2024-02-23 07:40:29'),
(143, 16, 7, '2024-02-23 07:40:59'),
(144, 16, 5, '2024-02-23 07:42:40'),
(145, 16, 9, '2024-02-23 07:43:16'),
(146, 16, 12, '2024-02-23 07:43:21'),
(147, 16, 6, '2024-02-23 07:43:44'),
(148, 16, 8, '2024-02-23 07:43:50'),
(149, 16, 5, '2024-02-23 07:44:57'),
(150, 16, 1, '2024-02-23 07:46:30'),
(151, 16, 5, '2024-02-23 07:48:08'),
(152, 16, 7, '2024-02-23 07:48:13'),
(153, 16, 1, '2024-02-23 07:48:32'),
(154, 16, 7, '2024-02-23 07:48:38'),
(155, 16, 9, '2024-02-23 07:49:24'),
(156, 16, 5, '2024-02-23 07:50:56'),
(157, 16, 12, '2024-02-23 07:54:13'),
(158, 16, 5, '2024-02-23 07:54:40'),
(159, 16, 5, '2024-02-23 07:57:25'),
(160, 16, 12, '2024-02-23 07:58:33');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `online` varchar(1) NOT NULL DEFAULT '0',
  `activation` varchar(3) NOT NULL DEFAULT 'yes'
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `mobile`, `reg_time`, `online`, `activation`) VALUES
(17, 'Asim Adhikari', 'aseemadhikari67@gmail.com', 'asimac', '$5$rounds=535000$/sqC7NU658h9QbVg$Ci7ZzJDU8phNqBkl1cpcDc2TjzZDFx8YTclBqg0omV6', '9808106688111', '2024-02-22 13:53:54', '0', 'yes'),
(15, 'Sujon', 'sujon@yahoo.com', 'sujons', '$5$rounds=535000$aGykDT1yrocgTaDt$p2dDAMDz9g3N6o/Jj7QJY9B6NnMlUot.DCq/LOsCS13', '89345793753', '2024-02-16 18:15:00', '0', 'yes'),
(16, 'Ashish Adhikari', 'acaashish08@gmail.com', 'ashishac', '$5$rounds=535000$FhMk2cK7aQkbTmK/$iniAviA1gIjPJuJ28Y2BgfeFs08ZbK5ylTOLYEABx97', '9813672338111', '2024-02-09 17:50:44', '1', 'yes');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_level`
--
ALTER TABLE `product_level`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_view`
--
ALTER TABLE `product_view`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `product_level`
--
ALTER TABLE `product_level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `product_view`
--
ALTER TABLE `product_view`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=161;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

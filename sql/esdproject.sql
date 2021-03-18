-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 17, 2021 at 03:56 PM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `esdproject`
--

-- --------------------------------------------------------

--
-- Table structure for table `pokemoncard`
--

DROP TABLE IF EXISTS `pokemoncard`;
CREATE TABLE IF NOT EXISTS `pokemoncard` (
  `card_id` varchar(13) NOT NULL,
  `seller_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `level` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `price` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pokemoncard`
--

INSERT INTO `pokemoncard` (`card_id`, `seller_id`, `name`, `level`, `image`, `price`) VALUES
('1', '1', 'charizard', '100', 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png', '100.00');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` varchar(13) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `telegram_id` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `name`, `email`, `telegram_id`, `phone_number`, `password`) VALUES
('1', 'Ash', 'ash@pokemon.com', '@GottaKetchup', '90909090', 'LetMePassESM');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2024 at 02:14 PM
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
-- Database: `agroconnect`
--

-- --------------------------------------------------------

--
-- Table structure for table `area`
--

CREATE TABLE `area` (
  `area_id` int(11) NOT NULL,
  `area_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `area`
--

INSERT INTO `area` (`area_id`, `area_name`) VALUES
(1, 'Mayyanad'),
(2, 'Kollam');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `customer_name` varchar(75) NOT NULL,
  `address` varchar(200) NOT NULL,
  `adhaar` varchar(16) NOT NULL,
  `mobileno` varchar(12) NOT NULL,
  `email` varchar(100) NOT NULL,
  `reg_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `area_id`, `customer_name`, `address`, `adhaar`, `mobileno`, `email`, `reg_date`) VALUES
(1, 2, 'Sachin', 'Sachin villa \r\nKollam', '2536541253653', '9875898589', 'sachin@gmail.com', '2024-11-03'),
(2, 1, 'asdfasf', 'wefasdf', '234525', '7868798', 'ss@gmail.com', '2024-11-03');

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `farmer_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `farmer_name` varchar(75) NOT NULL,
  `address` varchar(200) NOT NULL,
  `gender` varchar(12) NOT NULL,
  `adhaarno` varchar(16) NOT NULL,
  `mobile` varchar(12) NOT NULL,
  `email` varchar(100) NOT NULL,
  `reg_date` date NOT NULL,
  `upload` varchar(200) NOT NULL,
  `status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`farmer_id`, `area_id`, `farmer_name`, `address`, `gender`, `adhaarno`, `mobile`, `email`, `reg_date`, `upload`, `status`) VALUES
(1, 1, 'sdfgsdgsad', 'sdfasgsdg', 'on', '32542352', '2354235', 'ss@gmail.com', '2024-11-03', 'abstract.pdf', 'Register'),
(2, 2, 'Sumesh', 'sdgsag', 'on', '7868778', '6525415263', 'sumesh@gmail.com', '2024-11-03', 'Shijoy_State_Bank_Collect.pdf', 'Register');

-- --------------------------------------------------------

--
-- Table structure for table `land_owners`
--

CREATE TABLE `land_owners` (
  `landowner_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `landowner_name` varchar(75) NOT NULL,
  `address` varchar(200) NOT NULL,
  `adhaar` varchar(16) NOT NULL,
  `mobile` varchar(12) NOT NULL,
  `email` varchar(75) NOT NULL,
  `reg_date` date NOT NULL,
  `upload` varchar(200) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_owners`
--

INSERT INTO `land_owners` (`landowner_id`, `area_id`, `landowner_name`, `address`, `adhaar`, `mobile`, `email`, `reg_date`, `upload`, `status`) VALUES
(1, 1, 'Anil', 'Anil nivas', '213212', '121132132', 'ammu@gmail.com', '2024-11-03', 'abstract.pdf', 'Register');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL,
  `reg_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`login_id`, `reg_id`, `username`, `password`, `type`) VALUES
(1, 0, 'admin', 'admin', 'admin'),
(2, 1, 'ss@gmail.com', 'sdfgsdgsad123', 'farmer'),
(3, 2, 'sumesh@gmail.com', 'Sumesh123', 'farmer'),
(4, 1, 'ammu@gmail.com', 'Anil123', 'landowner'),
(5, 1, 'sachin@gmail.com', '', 'customer'),
(6, 2, 'ss@gmail.com', 'asd123', 'customer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`area_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`farmer_id`);

--
-- Indexes for table `land_owners`
--
ALTER TABLE `land_owners`
  ADD PRIMARY KEY (`landowner_id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`login_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `area`
--
ALTER TABLE `area`
  MODIFY `area_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `farmer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `land_owners`
--
ALTER TABLE `land_owners`
  MODIFY `landowner_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `login_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

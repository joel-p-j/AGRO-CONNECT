-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 08:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

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
-- Table structure for table `application_process`
--

CREATE TABLE `application_process` (
  `process_id` int(11) NOT NULL,
  `loan_app_id` int(11) NOT NULL,
  `admin_reply` varchar(200) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_process`
--

INSERT INTO `application_process` (`process_id`, `loan_app_id`, `admin_reply`, `date`) VALUES
(1, 1, 'anock ...your application is on processing....', '2025-03-18'),
(2, 3, 'steeve...your application is on processing....', '2025-03-18');

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
(2, 'Kollam'),
(5, 'mynagappally'),
(7, 'Kundara'),
(8, 'karunagappally'),
(9, 'Trivandrum'),
(17, 'Kilimanoor');

-- --------------------------------------------------------

--
-- Table structure for table `bill_payment`
--

CREATE TABLE `bill_payment` (
  `bill_payment_id` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `payment_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bill_payment`
--

INSERT INTO `bill_payment` (`bill_payment_id`, `bill_id`, `amount`, `payment_date`) VALUES
(1, 1, 460, '2025-03-24'),
(2, 2, 130, '2025-03-24'),
(3, 3, 665, '2025-03-28'),
(4, 4, 130, '2025-03-29'),
(5, 5, 540, '2025-03-29'),
(6, 6, 80, '2025-03-29');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `total_amount` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `customer_id`, `total_amount`, `date`, `status`) VALUES
(6, 1, 215, '2025-03-28', 'send');

-- --------------------------------------------------------

--
-- Table structure for table `cart_log`
--

CREATE TABLE `cart_log` (
  `cart_log_id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `rate` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart_log`
--

INSERT INTO `cart_log` (`cart_log_id`, `cart_id`, `product_id`, `quantity`, `rate`) VALUES
(1, 2, 2, 1.00, 50.00),
(2, 2, 3, 2.00, 80.00),
(3, 2, 4, 1.00, 250.00),
(4, 3, 2, 1.00, 50.00),
(5, 3, 3, 1.00, 80.00),
(7, 5, 2, 1.00, 50.00),
(8, 5, 4, 1.00, 250.00),
(9, 5, 4, 1.00, 250.00),
(10, 5, 1, 1.00, 40.00),
(11, 5, 15, 1.00, 75.00),
(13, 7, 2, 1.00, 50.00),
(14, 7, 3, 1.00, 80.00),
(15, 8, 4, 1.00, 250.00),
(16, 8, 4, 1.00, 250.00),
(17, 8, 1, 1.00, 40.00),
(18, 9, 3, 1.00, 80.00),
(19, 6, 15, 1.00, 75.00),
(20, 6, 1, 1.00, 40.00),
(21, 6, 2, 1.00, 50.00);

-- --------------------------------------------------------

--
-- Table structure for table `complaints`
--

CREATE TABLE `complaints` (
  `complaint_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `sender_type` varchar(50) NOT NULL,
  `to_person_id` int(11) NOT NULL,
  `to_person_type` varchar(50) NOT NULL,
  `complaint` varchar(150) NOT NULL,
  `date` date NOT NULL,
  `admin_reply` varchar(150) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `complaints`
--

INSERT INTO `complaints` (`complaint_id`, `sender_id`, `sender_type`, `to_person_id`, `to_person_type`, `complaint`, `date`, `admin_reply`, `status`) VALUES
(1, 1, 'Farmer', 1, 'Customer', 'anock complained nandu', '2025-02-11', '', 'enquiry sent'),
(2, 1, 'Farmer', 2, 'Customer', 'anock complained sachin', '2025-02-11', 'issue solved', 'Completed');

-- --------------------------------------------------------

--
-- Table structure for table `complaint_enquiry`
--

CREATE TABLE `complaint_enquiry` (
  `enquiry_id` int(11) NOT NULL,
  `complaint_id` int(11) NOT NULL,
  `enquiry` varchar(150) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `complaint_enquiry`
--

INSERT INTO `complaint_enquiry` (`enquiry_id`, `complaint_id`, `enquiry`, `date`, `status`) VALUES
(1, 1, 'anock enquired sachin', '2025-02-11', 'reply sent'),
(2, 2, 'anock enquired nandu', '2025-02-11', 'reply sent'),
(3, 3, 'anock enquired anil', '2025-02-11', 'Sent'),
(4, 4, 'anock enquired akash', '2025-02-11', 'Sent'),
(5, 5, 'nandu enquired anock', '2025-02-11', 'reply sent'),
(6, 6, 'sachin enquired steeve', '2025-02-11', 'reply sent'),
(7, 7, 'anil enquired anock', '2025-02-11', 'reply sent'),
(8, 8, 'akash enquired steeve', '2025-02-11', 'reply sent'),
(9, 9, 'steeve enquired nandu', '2025-02-11', 'reply sent'),
(10, 10, 'nandu enquired anock', '2025-03-10', 'Sent');

-- --------------------------------------------------------

--
-- Table structure for table `confirmation`
--

CREATE TABLE `confirmation` (
  `confir_id` int(11) NOT NULL,
  `enquiry_reply_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `account_holder_name` varchar(25) NOT NULL,
  `account_no` varchar(50) NOT NULL,
  `IFSC_code` varchar(25) NOT NULL,
  `branch_name` varchar(25) NOT NULL,
  `reg_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `area_id`, `customer_name`, `address`, `adhaar`, `mobileno`, `email`, `account_holder_name`, `account_no`, `IFSC_code`, `branch_name`, `reg_date`) VALUES
(1, 5, 'Nandu M', 'Nandu Bhavanam, Kadappa, Mynagappally', '789056433456', '8680976543', 'nandum143@gmail.com', 'Nandu M', '951627538641263', 'FDB1010', 'Sasthamcotta', '2025-03-28'),
(2, 9, 'Stella George', 'Stella Dale, Kilimanoor, Trivandrum', '546723459876', '9876543210', 'stellageorge231@gmail.com', 'Stella George', '984651324657653', 'CNRB4512', 'Kilimanoor', '2025-03-28');

-- --------------------------------------------------------

--
-- Table structure for table `customer_bill`
--

CREATE TABLE `customer_bill` (
  `bill_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `bill_no` varchar(20) NOT NULL,
  `bill_amount` decimal(11,2) NOT NULL,
  `payment_status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_bill`
--

INSERT INTO `customer_bill` (`bill_id`, `order_id`, `bill_no`, `bill_amount`, `payment_status`) VALUES
(1, 1, 'INV-001', 460.00, 'Paid'),
(2, 2, 'INV-002', 130.00, 'Paid'),
(3, 3, 'INV-003', 665.00, 'Paid'),
(4, 4, 'INV-004', 130.00, 'Paid'),
(5, 5, 'INV-005', 540.00, 'Paid'),
(6, 6, 'INV-006', 80.00, 'Paid');

-- --------------------------------------------------------

--
-- Table structure for table `enquiry_reply`
--

CREATE TABLE `enquiry_reply` (
  `enq_reply_id` int(11) NOT NULL,
  `enquiry_id` int(11) NOT NULL,
  `reply` varchar(150) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(15) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enquiry_reply`
--

INSERT INTO `enquiry_reply` (`enq_reply_id`, `enquiry_id`, `reply`, `date`, `status`) VALUES
(1, 5, 'anock replied nandu', '2025-02-11', 'Replied'),
(2, 7, 'anock replied anil', '2025-02-11', 'Replied'),
(3, 6, 'steeve enquired sachin', '2025-02-11', 'Replied'),
(4, 8, 'steeve replied akash', '2025-02-11', 'Sent'),
(5, 2, 'nandu replied anock', '2025-02-11', 'Replied'),
(6, 1, 'sachin replied anock', '2025-02-11', 'Sent'),
(7, 9, 'nandu replied steeve', '2025-02-11', 'Sent');

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `farmer_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `farmer_name` varchar(75) NOT NULL,
  `address` varchar(200) NOT NULL,
  `adhaarno` varchar(16) NOT NULL,
  `mobile` varchar(12) NOT NULL,
  `email` varchar(100) NOT NULL,
  `reg_date` date NOT NULL,
  `upload` varchar(200) NOT NULL,
  `account_holder_name` varchar(50) NOT NULL,
  `account_no` varchar(50) NOT NULL,
  `IFSC_code` varchar(25) NOT NULL,
  `branch_name` varchar(50) NOT NULL,
  `status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`farmer_id`, `area_id`, `farmer_name`, `address`, `adhaarno`, `mobile`, `email`, `reg_date`, `upload`, `account_holder_name`, `account_no`, `IFSC_code`, `branch_name`, `status`) VALUES
(1, 8, 'Anock Philip', 'Nathanya, Panayannarkav, Karunagappally', '658965323214', '7560864357', 'anocknathanya27@gmail.com', '2025-03-28', 'adhaar.pdf', 'Anock Philip', '450422430000450', 'CNRB4504', 'Karunagappally', 'Register'),
(2, 9, 'Steeve Roy', 'Galeria, Kakkanadu, Trivandrum', '325698741245', '8752364515', 'steeve123@gmail.com', '2025-03-28', 'adhaar.pdf', 'Steeve Roy', '987456321852963', 'SBI56012', 'kakkanadu', 'Register'),
(3, 1, 'stelin', 'tmkrkkrmkry', '546723459876', '9874563214', 'stelin34@gmail.com', '2025-03-30', 'adhaar.pdf', 'stelin', '450422430000567', 'CNRB4512', 'kakkanadu', 'Register');

-- --------------------------------------------------------

--
-- Table structure for table `farmerwisebill`
--

CREATE TABLE `farmerwisebill` (
  `farmer_bill_id` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmerwisebill`
--

INSERT INTO `farmerwisebill` (`farmer_bill_id`, `bill_id`, `order_id`, `farmer_id`, `amount`, `status`) VALUES
(1, 1, 1, 1, 210.00, 'Paid'),
(2, 1, 1, 2, 250.00, 'Paid'),
(3, 2, 2, 1, 130.00, 'Paid'),
(4, 3, 3, 1, 165.00, 'Paid'),
(5, 3, 3, 2, 500.00, 'Paid'),
(6, 4, 4, 1, 130.00, 'Paid'),
(7, 5, 5, 1, 40.00, 'Paid'),
(8, 5, 5, 2, 500.00, 'Paid'),
(9, 6, 6, 1, 80.00, 'Generated');

-- --------------------------------------------------------

--
-- Table structure for table `forms`
--

CREATE TABLE `forms` (
  `form_id` int(25) NOT NULL,
  `form_type` varchar(150) NOT NULL,
  `upload_form` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `forms`
--

INSERT INTO `forms` (`form_id`, `form_type`, `upload_form`) VALUES
(1, 'insurance', 'insurance_form.pdf'),
(2, 'loan', 'loan_form.pdf'),
(3, 'certificate', 'policy_certificate.pdf'),
(4, 'insurance_claim', 'insurance_claim_application.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `insurance_claim_request`
--

CREATE TABLE `insurance_claim_request` (
  `claim_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `policy_number` varchar(25) NOT NULL,
  `reason` varchar(300) NOT NULL,
  `upload` varchar(150) NOT NULL,
  `remark` varchar(400) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `insurance_claim_request`
--

INSERT INTO `insurance_claim_request` (`claim_id`, `farmer_id`, `policy_number`, `reason`, `upload`, `remark`, `date`, `status`) VALUES
(1, 1, 'PLC-001', 'pmfby by anock', 'insurance_claim_application.pdf', 'admin replied claimed insurance to anock', '2025-03-19', 'claimed');

-- --------------------------------------------------------

--
-- Table structure for table `insurance_type`
--

CREATE TABLE `insurance_type` (
  `insurance_type_id` int(11) NOT NULL,
  `insurance_type_name` varchar(150) NOT NULL,
  `premium_amount` varchar(15) NOT NULL,
  `coverage_amount` varchar(15) NOT NULL,
  `policy_terms` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `insurance_type`
--

INSERT INTO `insurance_type` (`insurance_type_id`, `insurance_type_name`, `premium_amount`, `coverage_amount`, `policy_terms`) VALUES
(1, 'Pradhan Mantri Fasal Bima Yojana (PMFBY)', '5000 Rs', '1,50,000Rs', '1 year'),
(2, 'Weather-Based Crop Insurance Scheme (WBCIS)', '1000 Rs', '25,000 Rs', '6 months'),
(3, 'Multi-Peril Crop Insurance (MPCI)', '500 Rs', '1,00,000Rs', '6 month'),
(4, 'Cattle Insurance', '200 Rs', '40,000 Rs', '1 year'),
(5, 'Poultry Insurance	', '₹10-₹15 per bir', '₹100-₹500 per b', '1 year'),
(6, 'Sheep/Goat Insurance', '1000Rs', '₹3,000-₹10,000 ', '1year'),
(7, 'Rubber Plantation Insurance', '200Rs per tree ', '50,000Rs', '1 year'),
(8, 'Fruit Crop Insurance (Mango, Apple, etc.)', '300 Rs per tree', '60,000 Rs', '6 months');

-- --------------------------------------------------------

--
-- Table structure for table `land_details`
--

CREATE TABLE `land_details` (
  `land_details_id` int(11) NOT NULL,
  `land_owner_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `village_name` varchar(75) NOT NULL,
  `total_area` varchar(15) NOT NULL,
  `survey_no` varchar(50) NOT NULL,
  `land_type` varchar(50) NOT NULL,
  `upload` varchar(150) NOT NULL,
  `remark` varchar(500) NOT NULL,
  `status` varchar(70) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_details`
--

INSERT INTO `land_details` (`land_details_id`, `land_owner_id`, `area_id`, `village_name`, `total_area`, `survey_no`, `land_type`, `upload`, `remark`, `status`, `date`) VALUES
(1, 1, 1, 'Methilkad', '30cent', '123/45', 'Residential Land', 'll5.jpg', 'Its an residential land of 30 cent with survey no 123/45 in the village of Methilkad.', 'approved', '2025-02-21'),
(2, 1, 2, 'kundara', '50cent', '456/56', 'Agricultural Land', 'll4.jpg', 'its an agricultural land of 50 cent with survey number 456/56 in the village of kundara.', 'approved', '2025-02-21'),
(3, 2, 5, 'kadappa', '40cent', '567/89', 'Residential Land', 'landscape-3405617_960_720.jpg', 'its a commercial land of 40 cent with survey no 567/89 in the village of mynagappally', 'approved', '2025-02-21'),
(4, 2, 8, 'panayannarkavu', '60cent', '234/67', 'Residential Land', 'll1.png', 'its an agricultural land of 60 cent with survey number 234/67  in the village of panayannarkavu.', 'approved', '2025-02-21'),
(5, 2, 8, 'kundara', '70cent', '412/85', 'Agricultural Land', 'llkk.jpg', 'agricultural land of 70cent with survey no:412/85 ', 'approved', '2025-03-08'),
(6, 1, 2, 'kollam', '50cent', '789/09', 'Agricultural Land', 'landjj.jpg', '50 cent agricultural land in kollam town with survey number 789/09', 'Added', '2025-03-10');

-- --------------------------------------------------------

--
-- Table structure for table `land_enquiry`
--

CREATE TABLE `land_enquiry` (
  `land_enquiry_id` int(11) NOT NULL,
  `not_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `matter` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_enquiry`
--

INSERT INTO `land_enquiry` (`land_enquiry_id`, `not_id`, `farmer_id`, `matter`, `date`, `status`) VALUES
(1, 3, 1, 'its a commercial land of 40 cent with survey no 567/89 in the village of mynagappally\n\n', '2025-03-23', 'completed'),
(2, 2, 1, ' its an agricultural land of 50 cent with survey number 456/56 in the village of kundara.', '2025-03-23', 'Sent');

-- --------------------------------------------------------

--
-- Table structure for table `land_enquiry_confirmation`
--

CREATE TABLE `land_enquiry_confirmation` (
  `confirmation_id` int(11) NOT NULL,
  `enquiry_reply_id` int(11) NOT NULL,
  `mou_upload` varchar(200) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_enquiry_confirmation`
--

INSERT INTO `land_enquiry_confirmation` (`confirmation_id`, `enquiry_reply_id`, `mou_upload`, `status`) VALUES
(1, 1, 'Farm_Land_Cash_Lease_Agreement_5.pdf', 'confirm');

-- --------------------------------------------------------

--
-- Table structure for table `land_enquiry_reply`
--

CREATE TABLE `land_enquiry_reply` (
  `enquiry_reply_id` int(11) NOT NULL,
  `land_enquiry_id` int(11) NOT NULL,
  `reply` varchar(300) NOT NULL,
  `date` date NOT NULL,
  `MOU` varchar(800) NOT NULL,
  `lease_amount` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_enquiry_reply`
--

INSERT INTO `land_enquiry_reply` (`enquiry_reply_id`, `land_enquiry_id`, `reply`, `date`, `MOU`, `lease_amount`) VALUES
(1, 1, 'its a commercial land of 40 cent with survey no 567/89 in the village of mynagappally', '2025-03-23', 'Farm_Land_Cash_Lease_Agreement_5.pdf', '5000');

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
  `account_holder_name` varchar(50) NOT NULL,
  `account_no` varchar(50) NOT NULL,
  `IFSC_code` varchar(25) NOT NULL,
  `branch_name` varchar(25) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `land_owners`
--

INSERT INTO `land_owners` (`landowner_id`, `area_id`, `landowner_name`, `address`, `adhaar`, `mobile`, `email`, `reg_date`, `upload`, `account_holder_name`, `account_no`, `IFSC_code`, `branch_name`, `status`) VALUES
(1, 1, 'Feba Mathew', 'Gracia, Mayyanad, Kollam', '856325567412', '7412589632', 'febamathew432@gmail.com', '2025-03-28', 'adhaar.pdf', 'Feba Mathew', '968500789645253', 'SBI56122', 'Kundara', 'Register'),
(2, 2, 'Akash B', 'Akash Villa, Mulavana, Kundara', '856332567412', '7044637312', 'akashbprasad@gmail.com', '2025-03-28', 'adhaar.pdf', 'Akash B', '963852123852963', 'FDB1004', 'Kollam', 'Register');

-- --------------------------------------------------------

--
-- Table structure for table `lease_agreement_form`
--

CREATE TABLE `lease_agreement_form` (
  `lgform_id` int(11) NOT NULL,
  `mou_upload` varchar(100) NOT NULL,
  `type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lease_agreement_form`
--

INSERT INTO `lease_agreement_form` (`lgform_id`, `mou_upload`, `type`) VALUES
(1, 'Farm_Land_Cash_Lease_Agreement.pdf', 'lease agreement'),
(2, 'Lease_Agreement.pdf', 'lease agreement');

-- --------------------------------------------------------

--
-- Table structure for table `lease_payment`
--

CREATE TABLE `lease_payment` (
  `lease_payment_id` int(11) NOT NULL,
  `confirmation_id` int(11) NOT NULL,
  `amount` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lease_payment`
--

INSERT INTO `lease_payment` (`lease_payment_id`, `confirmation_id`, `amount`, `date`) VALUES
(1, 1, '5000', '2025-03-24');

-- --------------------------------------------------------

--
-- Table structure for table `loans`
--

CREATE TABLE `loans` (
  `loan_id` int(11) NOT NULL,
  `process_id` int(11) NOT NULL,
  `loan_amount` varchar(20) NOT NULL,
  `sanctioned_date` date NOT NULL,
  `loan_end_date` date NOT NULL,
  `emi_amount` varchar(20) NOT NULL,
  `remark` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loans`
--

INSERT INTO `loans` (`loan_id`, `process_id`, `loan_amount`, `sanctioned_date`, `loan_end_date`, `emi_amount`, `remark`) VALUES
(1, 1, '1,00,000 Rs', '2025-03-19', '2028-03-18', '10,000', 'Crop Loan (Kisan Credit Card - KCC) by Anock Philip. An amount of 1,00,000 Rs.'),
(2, 2, '2,00,000', '2025-03-19', '2027-03-19', '5000', 'Dairy and Animal Husbandry Loan by Steeve . An amount of 2,00,000.'),
(3, 1, '1,00,000 Rs', '2025-03-22', '2028-03-21', '5000', 'Crop Loan (Kisan Credit Card - KCC)  Anock Philip          \r\n Loan Amount : 1,00,000 Rs  \r\nEMI amoun');

-- --------------------------------------------------------

--
-- Table structure for table `loan_application`
--

CREATE TABLE `loan_application` (
  `loan_app_id` int(11) NOT NULL,
  `loan_type_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `loan_amount` varchar(15) NOT NULL,
  `upload` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loan_application`
--

INSERT INTO `loan_application` (`loan_app_id`, `loan_type_id`, `farmer_id`, `loan_amount`, `upload`, `date`, `status`) VALUES
(1, 1, 1, '1,00,000 Rs', 'loan_form.pdf', '2025-03-17', 'sanctioned'),
(2, 3, 2, '50,000', 'loan_form.pdf', '2025-03-17', 'sent'),
(3, 6, 2, '2,00,000', 'loan_form.pdf', '2025-03-17', 'sanctioned');

-- --------------------------------------------------------

--
-- Table structure for table `loan_type`
--

CREATE TABLE `loan_type` (
  `loan_type_id` int(11) NOT NULL,
  `scheme_name` varchar(150) NOT NULL,
  `terms_and_conditions` varchar(150) NOT NULL,
  `maximum_amount` varchar(50) NOT NULL,
  `maturity_period` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loan_type`
--

INSERT INTO `loan_type` (`loan_type_id`, `scheme_name`, `terms_and_conditions`, `maximum_amount`, `maturity_period`) VALUES
(1, 'Crop Loan (Kisan Credit Card - KCC)', 'Farmer_Loan_Terms.pdf', '3 lakh', '3 years'),
(2, 'Agriculture Term Loan', 'Farmer_Loan_Terms.pdf', '50,000 Rs', '1 year'),
(3, 'Dairy and Animal Husbandry Loan', 'Farmer_Loan_Terms.pdf', '20 lakh', '5 years'),
(4, 'Horticulture Loan', 'Farmer_Loan_Terms.pdf', '10 lakh', '7 years'),
(5, 'Farm Mechanization Loan', 'Farmer_Loan_Terms.pdf', '12 lakh', '6 years'),
(6, ' Agricultural Gold Loan', 'Farmer_Loan_Terms.pdf', '5 lakh', '2 years');

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
(2, 1, 'anocknathanya27@gmail.com', 'anock123', 'farmer'),
(3, 2, 'steeve123@gmail.com', 'steeve123', 'farmer'),
(4, 1, 'febamathew432@gmail.com', 'feba123', 'landowner'),
(5, 2, 'akashbprasad@gmail.com', 'akash123', 'landowner'),
(7, 1, 'nandum143@gmail.com', 'nandu123', 'customer'),
(8, 2, 'stellageorge231@gmail.com', 'stella123', 'customer'),
(9, 3, 'stelin34@gmail.com', 'stelin123', 'farmer');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `not_id` int(11) NOT NULL,
  `land_details_id` varchar(50) NOT NULL,
  `matter` varchar(500) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`not_id`, `land_details_id`, `matter`, `date`) VALUES
(1, '1', 'Its an residential land of 30 cent with survey no 123/45 in the village of Methilkad.', '2025-03-04'),
(2, '2', 'its an agricultural land of 50 cent with survey number 456/56 in the village of kundara.', '2025-03-04'),
(3, '3', 'its a commercial land of 40 cent with survey no 567/89 in the village of mynagappally', '2025-03-04'),
(4, '4', 'its an agricultural land of 60 cent with survey number 234/67  in the village of panayannarkavu.', '2025-03-04'),
(5, '5', 'karunagappally, Agricultural Land, 412/85, 70cent', '2025-03-22'),
(6, '3', 'Residential Land, 567/89, 40cent, mynagappally', '2025-03-22');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `order_no` varchar(25) NOT NULL,
  `total_amount` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `cart_id`, `customer_id`, `order_no`, `total_amount`, `date`, `status`) VALUES
(1, 2, 1, 'ODR-001', 460, '2025-03-24', 'Bill Generated'),
(2, 3, 1, 'ODR-002', 130, '2025-03-24', 'Bill Generated'),
(3, 5, 1, 'ODR-003', 665, '2025-03-28', 'Bill Generated'),
(4, 7, 2, 'ODR-004', 130, '2025-03-29', 'Bill Generated'),
(5, 8, 2, 'ODR-005', 540, '2025-03-29', 'Bill Generated'),
(6, 9, 2, 'ODR-006', 80, '2025-03-29', 'Bill Generated');

-- --------------------------------------------------------

--
-- Table structure for table `policy`
--

CREATE TABLE `policy` (
  `policy_id` int(11) NOT NULL,
  `p_application_id` int(11) NOT NULL,
  `policy_number` varchar(25) NOT NULL,
  `policy_details` varchar(250) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `policy_document` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy`
--

INSERT INTO `policy` (`policy_id`, `p_application_id`, `policy_number`, `policy_details`, `start_date`, `end_date`, `policy_document`) VALUES
(1, 1, 'PLC-001', 'Pradhan Mantri Fasal Bima Yojana (PMFBY)	Anock Philip', '2025-03-24', '2026-03-24', 'policy.pdf'),
(2, 2, 'PLC-002', 'Poultry Insurance	Steeve	', '2025-03-24', '2026-03-24', 'policy.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `policy_application`
--

CREATE TABLE `policy_application` (
  `p_application_id` int(11) NOT NULL,
  `insurance_type_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `upload` varchar(75) NOT NULL,
  `admin_reply` varchar(150) NOT NULL,
  `farmer_confirmation` varchar(200) NOT NULL,
  `status` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy_application`
--

INSERT INTO `policy_application` (`p_application_id`, `insurance_type_id`, `farmer_id`, `upload`, `admin_reply`, `farmer_confirmation`, `status`, `date`) VALUES
(1, 1, 1, 'insurance_form.pdf', 'replied', 'confirmed', 'completed', '2025-03-24'),
(2, 5, 2, 'insurance_form_5.pdf', 'replied', 'confirmed', 'completed', '2025-03-24');

-- --------------------------------------------------------

--
-- Table structure for table `policy_payment`
--

CREATE TABLE `policy_payment` (
  `payment_id` int(11) NOT NULL,
  `policy_id` int(11) NOT NULL,
  `amount` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `policy_payment`
--

INSERT INTO `policy_payment` (`payment_id`, `policy_id`, `amount`, `date`) VALUES
(1, 1, '5000 Rs', '2025-03-24'),
(2, 2, '₹10-₹15 per bir', '2025-03-24');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `pcategory_id` int(11) NOT NULL,
  `farmer_id` int(11) NOT NULL,
  `product_code` varchar(20) NOT NULL,
  `product_name` varchar(25) NOT NULL,
  `image` varchar(250) NOT NULL,
  `rate` varchar(25) NOT NULL,
  `quantity` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `pcategory_id`, `farmer_id`, `product_code`, `product_name`, `image`, `rate`, `quantity`) VALUES
(1, 1, 1, 'VEGTMT01', 'Tomato', 'tomato.png', '40', '1 kg'),
(2, 2, 1, 'FRTORG01', 'Orange', 'orange.jpg', '50', '1 kg'),
(3, 1, 1, 'VEGPOT02', 'potato', 'potato.png', '80', '2 kg'),
(4, 1, 2, 'VEGCRT03', 'carrot', 'carrot.png', '250', '5 kg'),
(5, 2, 2, 'FRTAPL02', 'Apple', 'apple.jpg', '100', '2 kg'),
(15, 1, 1, 'VEGONI03', 'onion', 'onion.png', '75', '1 kg'),
(16, 1, 3, 'VEGCRT05', 'carrot', 'carrot.png', '150', '5 kg');

-- --------------------------------------------------------

--
-- Table structure for table `product_category`
--

CREATE TABLE `product_category` (
  `pcategory_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_category`
--

INSERT INTO `product_category` (`pcategory_id`, `category_name`) VALUES
(1, 'vegetables'),
(2, 'fruits');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `application_process`
--
ALTER TABLE `application_process`
  ADD PRIMARY KEY (`process_id`);

--
-- Indexes for table `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`area_id`);

--
-- Indexes for table `bill_payment`
--
ALTER TABLE `bill_payment`
  ADD PRIMARY KEY (`bill_payment_id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- Indexes for table `cart_log`
--
ALTER TABLE `cart_log`
  ADD PRIMARY KEY (`cart_log_id`);

--
-- Indexes for table `complaints`
--
ALTER TABLE `complaints`
  ADD PRIMARY KEY (`complaint_id`);

--
-- Indexes for table `complaint_enquiry`
--
ALTER TABLE `complaint_enquiry`
  ADD PRIMARY KEY (`enquiry_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `customer_bill`
--
ALTER TABLE `customer_bill`
  ADD PRIMARY KEY (`bill_id`);

--
-- Indexes for table `enquiry_reply`
--
ALTER TABLE `enquiry_reply`
  ADD PRIMARY KEY (`enq_reply_id`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`farmer_id`);

--
-- Indexes for table `farmerwisebill`
--
ALTER TABLE `farmerwisebill`
  ADD PRIMARY KEY (`farmer_bill_id`);

--
-- Indexes for table `forms`
--
ALTER TABLE `forms`
  ADD PRIMARY KEY (`form_id`);

--
-- Indexes for table `insurance_claim_request`
--
ALTER TABLE `insurance_claim_request`
  ADD PRIMARY KEY (`claim_id`);

--
-- Indexes for table `insurance_type`
--
ALTER TABLE `insurance_type`
  ADD PRIMARY KEY (`insurance_type_id`);

--
-- Indexes for table `land_details`
--
ALTER TABLE `land_details`
  ADD PRIMARY KEY (`land_details_id`);

--
-- Indexes for table `land_enquiry`
--
ALTER TABLE `land_enquiry`
  ADD PRIMARY KEY (`land_enquiry_id`);

--
-- Indexes for table `land_enquiry_confirmation`
--
ALTER TABLE `land_enquiry_confirmation`
  ADD PRIMARY KEY (`confirmation_id`);

--
-- Indexes for table `land_enquiry_reply`
--
ALTER TABLE `land_enquiry_reply`
  ADD PRIMARY KEY (`enquiry_reply_id`);

--
-- Indexes for table `land_owners`
--
ALTER TABLE `land_owners`
  ADD PRIMARY KEY (`landowner_id`);

--
-- Indexes for table `lease_agreement_form`
--
ALTER TABLE `lease_agreement_form`
  ADD PRIMARY KEY (`lgform_id`);

--
-- Indexes for table `lease_payment`
--
ALTER TABLE `lease_payment`
  ADD PRIMARY KEY (`lease_payment_id`);

--
-- Indexes for table `loans`
--
ALTER TABLE `loans`
  ADD PRIMARY KEY (`loan_id`);

--
-- Indexes for table `loan_application`
--
ALTER TABLE `loan_application`
  ADD PRIMARY KEY (`loan_app_id`);

--
-- Indexes for table `loan_type`
--
ALTER TABLE `loan_type`
  ADD PRIMARY KEY (`loan_type_id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`login_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`not_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `policy`
--
ALTER TABLE `policy`
  ADD PRIMARY KEY (`policy_id`);

--
-- Indexes for table `policy_application`
--
ALTER TABLE `policy_application`
  ADD PRIMARY KEY (`p_application_id`);

--
-- Indexes for table `policy_payment`
--
ALTER TABLE `policy_payment`
  ADD PRIMARY KEY (`payment_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `product_category`
--
ALTER TABLE `product_category`
  ADD PRIMARY KEY (`pcategory_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `application_process`
--
ALTER TABLE `application_process`
  MODIFY `process_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `area`
--
ALTER TABLE `area`
  MODIFY `area_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `bill_payment`
--
ALTER TABLE `bill_payment`
  MODIFY `bill_payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `cart_log`
--
ALTER TABLE `cart_log`
  MODIFY `cart_log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `complaints`
--
ALTER TABLE `complaints`
  MODIFY `complaint_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `complaint_enquiry`
--
ALTER TABLE `complaint_enquiry`
  MODIFY `enquiry_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `customer_bill`
--
ALTER TABLE `customer_bill`
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `enquiry_reply`
--
ALTER TABLE `enquiry_reply`
  MODIFY `enq_reply_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `farmer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `farmerwisebill`
--
ALTER TABLE `farmerwisebill`
  MODIFY `farmer_bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `forms`
--
ALTER TABLE `forms`
  MODIFY `form_id` int(25) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `insurance_claim_request`
--
ALTER TABLE `insurance_claim_request`
  MODIFY `claim_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `insurance_type`
--
ALTER TABLE `insurance_type`
  MODIFY `insurance_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `land_details`
--
ALTER TABLE `land_details`
  MODIFY `land_details_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `land_enquiry`
--
ALTER TABLE `land_enquiry`
  MODIFY `land_enquiry_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `land_enquiry_confirmation`
--
ALTER TABLE `land_enquiry_confirmation`
  MODIFY `confirmation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `land_enquiry_reply`
--
ALTER TABLE `land_enquiry_reply`
  MODIFY `enquiry_reply_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `land_owners`
--
ALTER TABLE `land_owners`
  MODIFY `landowner_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `lease_agreement_form`
--
ALTER TABLE `lease_agreement_form`
  MODIFY `lgform_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `lease_payment`
--
ALTER TABLE `lease_payment`
  MODIFY `lease_payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `loans`
--
ALTER TABLE `loans`
  MODIFY `loan_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `loan_application`
--
ALTER TABLE `loan_application`
  MODIFY `loan_app_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `loan_type`
--
ALTER TABLE `loan_type`
  MODIFY `loan_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `login_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `not_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `policy`
--
ALTER TABLE `policy`
  MODIFY `policy_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `policy_application`
--
ALTER TABLE `policy_application`
  MODIFY `p_application_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `policy_payment`
--
ALTER TABLE `policy_payment`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `product_category`
--
ALTER TABLE `product_category`
  MODIFY `pcategory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

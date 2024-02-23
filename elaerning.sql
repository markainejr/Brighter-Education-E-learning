-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2024 at 03:57 PM
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
-- Database: `elaerning`
--

-- --------------------------------------------------------

--
-- Table structure for table `barner`
--

CREATE TABLE `barner` (
  `bar_id` int(11) NOT NULL,
  `name` varchar(250) NOT NULL,
  `img` varchar(250) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barner`
--

INSERT INTO `barner` (`bar_id`, `name`, `img`, `description`) VALUES
(1, 'It\'s time to amplify your online education', 'static/uploads/2802694.jpg', 'Here is your best chance ');

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE `log` (
  `user_id` int(11) NOT NULL,
  `name` varchar(250) NOT NULL,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `retype` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log`
--

INSERT INTO `log` (`user_id`, `name`, `username`, `password`, `retype`) VALUES
(1, 'hamk', 'hamk', '12345', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE `results` (
  `results_id` int(11) NOT NULL,
  `term_one` varchar(250) NOT NULL,
  `term_two` varchar(250) NOT NULL,
  `term_three` varchar(250) NOT NULL,
  `comments` text NOT NULL,
  `students_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`results_id`, `term_one`, `term_two`, `term_three`, `comments`, `students_id`) VALUES
(1, '50', '50', '50', '2', 0),
(2, '50', '50', '50', '2', 0),
(3, '80', '60', '99', '3', 0);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `students_id` int(11) NOT NULL,
  `full_name` varchar(250) NOT NULL,
  `class` varchar(250) NOT NULL,
  `address` varchar(250) NOT NULL,
  `parent_name` varchar(250) NOT NULL,
  `contact` varchar(200) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`students_id`, `full_name`, `class`, `address`, `parent_name`, `contact`, `username`, `password`) VALUES
(1, 'Ham kalanzi', 'S2', 'Gayaza', 'hamk', '0772819744', 'hamk', '12345'),
(2, 'John Kagwa', 'S1', 'Mukono', 'Mujib', '0773456567', 'admin', '12345'),
(3, 'Michael Kiganda', 'S2', 'Gayaza', 'Mujib', '0772819744', 'hamid', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `sub_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `subjects` varchar(250) NOT NULL,
  `outline` text NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`sub_id`, `date`, `subjects`, `outline`, `description`) VALUES
(1, '2024-02-20', 'Physics', 'hhhhhhhhhhhhhhh', 'its a science subject..'),
(2, '2024-02-20', 'Mathmatics', 'it involves calculations ', 'its both science and arts subject'),
(3, '2024-02-20', 'Biology ', 'it involves calculations ', 'its nnnnnnnnnn');

-- --------------------------------------------------------

--
-- Table structure for table `topics`
--

CREATE TABLE `topics` (
  `topic_id` int(11) NOT NULL,
  `class1` varchar(250) NOT NULL,
  `term` varchar(250) NOT NULL,
  `img` varchar(250) NOT NULL,
  `body` text NOT NULL,
  `duration` varchar(250) NOT NULL,
  `sub_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `topics`
--

INSERT INTO `topics` (`topic_id`, `class1`, `term`, `img`, `body`, `duration`, `sub_id`) VALUES
(2, 'S3', 'Two', 'static/uploads/4483048.jpg', 'We upload tutorials of all our subjects as per curriculum.', '2hours', 3),
(3, 'S4', 'One', 'static/uploads/7949221.jpg', 'Popular Online Subjects Around You', '34', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barner`
--
ALTER TABLE `barner`
  ADD PRIMARY KEY (`bar_id`);

--
-- Indexes for table `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `results`
--
ALTER TABLE `results`
  ADD PRIMARY KEY (`results_id`),
  ADD KEY `results_id` (`results_id`,`term_one`,`term_two`,`term_three`),
  ADD KEY `comments` (`comments`(768));

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`students_id`),
  ADD KEY `students_id` (`students_id`,`full_name`,`class`),
  ADD KEY `address` (`address`,`parent_name`,`contact`),
  ADD KEY `username` (`username`,`password`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`sub_id`),
  ADD KEY `subjects_id` (`sub_id`,`date`,`subjects`),
  ADD KEY `description` (`description`(768)),
  ADD KEY `outline` (`outline`(768));

--
-- Indexes for table `topics`
--
ALTER TABLE `topics`
  ADD PRIMARY KEY (`topic_id`),
  ADD KEY `body` (`body`(768)),
  ADD KEY `img` (`img`),
  ADD KEY `topic_id` (`topic_id`,`sub_id`),
  ADD KEY `duration` (`duration`),
  ADD KEY `class` (`class1`,`term`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barner`
--
ALTER TABLE `barner`
  MODIFY `bar_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `log`
--
ALTER TABLE `log`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `results`
--
ALTER TABLE `results`
  MODIFY `results_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `students_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `sub_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `topics`
--
ALTER TABLE `topics`
  MODIFY `topic_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

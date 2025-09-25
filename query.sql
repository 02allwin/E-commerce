
CREATE DATABASE local_event_finder;
USE local_event_finder;

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL,
  `servicer_user_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `booker_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `address` text NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `guests` int(11) DEFAULT NULL,
  `dj_name` varchar(100) DEFAULT NULL,
  `theme` varchar(255) DEFAULT NULL,
  `birthday_age` int(11) DEFAULT NULL,
  `price` int(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `service_id` (`service_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE CASCADE,
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

LOCK TABLES `bookings` WRITE;
REPLACE INTO `bookings` (`booking_id`, `service_id`, `servicer_user_id`, `user_id`, `booker_name`, `email`, `mobile`, `address`, `category_name`, `date`, `time`, `guests`, `dj_name`, `theme`, `birthday_age`, `price`) VALUES
(2, 1, 2, 2, 'dfg', 'gdfgfd@sdfsd', '4535345', 'sfdsdf', 'DJ Services', '2025-05-02', '15:07:00', NULL, 'sdf', NULL, NULL, 1000);
UNLOCK TABLES;

CREATE TABLE `booking_status` (
  `status_id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) NOT NULL,
  `status` varchar(255) DEFAULT 'PENDING',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`status_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `booking_status_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE
);

LOCK TABLES `booking_status` WRITE;
REPLACE INTO `booking_status` (`status_id`, `booking_id`, `status`, `created_at`) VALUES
(2, 2, 'ACCEPT', '2025-05-05 15:07:17');
UNLOCK TABLES;

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `review` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `service_id` (`service_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

CREATE TABLE `service` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(255) NOT NULL,
  `service_description` text NOT NULL,
  `service_price` decimal(10,2) NOT NULL,
  `service_image` text NOT NULL,
  `city_pincode` varchar(10) NOT NULL,
  `service_address` text NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `servicers_user_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_id`),
  KEY `servicers_user_id` (`servicers_user_id`),
  KEY `city_pincode` (`city_pincode`),
  CONSTRAINT `service_ibfk_1` FOREIGN KEY (`servicers_user_id`) REFERENCES `servicers_details` (`servicers_user_id`) ON DELETE CASCADE,
  CONSTRAINT `service_ibfk_2` FOREIGN KEY (`city_pincode`) REFERENCES `service_city` (`city_pincode`) ON DELETE CASCADE
);

LOCK TABLES `service` WRITE;
REPLACE INTO `service` (`service_id`, `service_name`, `service_description`, `service_price`, `service_image`, `city_pincode`, `service_address`, `category_id`, `servicers_user_id`, `created_at`) VALUES
(1, 'SPB', 'SPB is a best thanjavur services ', 1000, '/media/dj_service_KXDUFRl.jpg', '613001', 'Thanjavur , NewBustand TamilNadu', 3, 2, '2025-05-05 13:24:11');
UNLOCK TABLES;

CREATE TABLE `servicers_details` (
  `servicers_user_id` int(11) NOT NULL AUTO_INCREMENT,
  `servicers_name` varchar(255) NOT NULL,
  `servicers_mobile` varchar(20) NOT NULL,
  `servicers_email` varchar(255) NOT NULL,
  `servicers_password` varchar(50) DEFAULT NULL,
  `servicers_address` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`servicers_user_id`),
  UNIQUE KEY `servicers_mobile` (`servicers_mobile`),
  UNIQUE KEY `servicers_email` (`servicers_email`)
);

LOCK TABLES `servicers_details` WRITE;
REPLACE INTO `servicers_details` (`servicers_user_id`, `servicers_name`, `servicers_mobile`, `servicers_email`, `servicers_password`, `servicers_address`, `created_at`) VALUES
(2, 'Prem', '8072620523', 'prem@gmail.com', '1234', NULL, '2025-05-03 16:41:30');
UNLOCK TABLES;

CREATE TABLE `services_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
);

LOCK TABLES `services_category` WRITE;
REPLACE INTO `services_category` (`category_id`, `category_name`, `created_at`) VALUES
(2, 'wedding', '2025-05-05 13:23:01'),
(3, 'DJ Services', '2025-05-05 13:35:23');
UNLOCK TABLES;

CREATE TABLE `service_city` (
  `service_city_id` int(11) NOT NULL AUTO_INCREMENT,
  `city_pincode` varchar(10) NOT NULL,
  `city_name` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_city_id`),
  UNIQUE KEY `city_pincode` (`city_pincode`)
);

LOCK TABLES `service_city` WRITE;
REPLACE INTO `service_city` (`service_city_id`, `city_pincode`, `city_name`, `created_at`) VALUES
(5, '613001', 'Thanjavur', '2025-05-03 21:43:17');
UNLOCK TABLES;

CREATE TABLE `service_details` (
  `servicers_id` int(11) NOT NULL AUTO_INCREMENT,
  `servicers_user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`servicers_id`),
  KEY `servicers_user_id` (`servicers_user_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `service_details_ibfk_1` FOREIGN KEY (`servicers_user_id`) REFERENCES `servicers_details` (`servicers_user_id`) ON DELETE CASCADE,
  CONSTRAINT `service_details_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `services_category` (`category_id`) ON DELETE CASCADE
);

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(25) NOT NULL,
  `user_email` varchar(25) NOT NULL,
  `user_password` varchar(25) NOT NULL,
  `user_mobile` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
);



LOCK TABLES `users` WRITE;
REPLACE INTO `users` (`user_id`, `user_name`, `user_email`, `user_password`, `user_mobile`, `reg_date`) VALUES
(2, 'prem', 'rajp37590@gmail.com', '1234', '8072620523', '2025-05-03 16:40:38');
UNLOCK TABLES;

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- START TRANSACTION;
-- SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `shippingDB`;
CREATE DATABASE IF NOT EXISTS `shippingDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use `shippingDB`;

create table `shipment`
(`ship_id` int not null primary key AUTO_INCREMENT,
`payment_id` int not null, 
`shipping_status` varchar(10) not null default "PENDING",
`receive_status` varchar(10) not null default "PENDING",
`created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table `shipping_details` 
(`ship_id` int not null primary key,
`order_id` int not null,
`seller_id` int not null,
`buyer_id` int not null, 
constraint `shipping_details_fk` foreign key(`ship_id`) references `shipment`(`ship_id`)
); 

-- create table `contact`
-- (`ship_id` int not null primary key,
-- `seller_chat_id` int not null, 
-- `buyer_chat_id` int not null,
-- constraint `contact_fk` foreign key(`ship_id`) references `shipment`(`ship_id`)
-- );

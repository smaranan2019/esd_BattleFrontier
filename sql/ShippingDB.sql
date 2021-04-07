-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- START TRANSACTION;
-- SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `shippingDB`;
CREATE DATABASE IF NOT EXISTS `shippingDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use `shippingDB`;

create table `shipping`
(`shipping_id` int not null primary key AUTO_INCREMENT,
`payment_id` int not null, 
`shipping_status` varchar(10) not null default "PENDING",
`receive_status` varchar(10) not null default "PENDING",
`created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table `shipping_details` 
(`shipping_id` int not null primary key,
`order_id` int not null,
`seller_id` int not null,
`buyer_id` int not null, 
constraint `shipping_details_fk` foreign key(`shipping_id`) references `shipping`(`shipping_id`)
); 

insert into `shipping`(`payment_id`, `shipping_status`) values 
(2, "SHIPPED"),
(3, "PENDING");

insert into `shipping_details` (`shipping_id`, `order_id`, `seller_id`, `buyer_id`) values 
((select shipping_id from `shipping` where payment_id = 2), 2, 2, 1),
((select shipping_id from `shipping` where payment_id = 3), 3, 2, 1);

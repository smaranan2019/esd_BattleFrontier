SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `orderDB`;
CREATE DATABASE IF NOT EXISTS `orderDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use `orderDB`;

create table `order` 
(`order_id` int not null primary key AUTO_INCREMENT,
`buyer_id` int not null, 
# `status` varchar(10) not null default "NEW",
`created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
`seller_id` int not null, 
`price` numeric(4,2) not null) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8; 

create table `item`
(`order_id` int not null primary key,
`card_id` int not null,
`quantity` int not null,
constraint `item_fk` foreign key(`order_id`) references `order`(`order_id`) on delete cascade on update cascade
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table `contact`
(`order_id` int not null primary key,
`seller_chat_id` int not null,
`buyer_chat_id` int not null,
constraint `contact_fk` foreign key(`order_id`) references `order`(`order_id`) on delete cascade on update cascade
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

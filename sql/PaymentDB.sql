SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `paymentDB`;
CREATE DATABASE IF NOT EXISTS `paymentDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use `paymentDB`;

create table `payment`
(`payment_id` int not null primary key AUTO_INCREMENT, 
`order_id` int not null,   
`payment_status` varchar(10) not null default "NEW",
`refund_status` varchar(10) not null "NULL",
`created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
`modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table `payment_details`
(`payment_id` int not null primary key,
`amount` numeric(4,2) not null, 
`seller_id` int not null, 
`buyer_id` int not null,
constraint `payment_details_fk` foreign key(`payment_id`) references `payment`(`payment_id`) on delete cascade on update cascade
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table `contact`
(`payment_id` int not null primary key,
`seller_chat_id` int not null,
`buyer_chat_id` int not null,
constraint `contact_fk` foreign key(`payment_id`) references `payment`(`payment_id`) on delete cascade on update cascade
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

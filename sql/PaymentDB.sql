DROP DATABASE IF EXISTS PaymentDB;
CREATE DATABASE PaymentDB;
use PaymentDB;

create table Payment
(PaymentID int not null primary key AUTO_INCREMENT, 
orderID int not null,   
status varchar(255),
created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table PaymentDetails
(PaymentID int not null primary key,
Amount decimal(3,2) not null, 
SellerID int not null, 
BuyerID int not null
);

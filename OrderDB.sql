DROP DATABASE IF EXISTS OrderDB;
CREATE DATABASE OrderDB;
use OrderDB;

create table OrderForm 
(OrderID int not null primary key AUTO_INCREMENT,
BuyerID int not null, 
created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
SellerID int not null, 
Price decimal(3,2) not null 
);

create table Item
(OrderID int not null primary key,
CardID int not null,
quantity int not null,
constraint Item_fk foreign key(OrderID) references OrderForm(OrderID)
);

create table Contact
(OrderID int not null primary key,
seller_chatID varchar(255) not null,
buyer_chatID varchar(255) not null 
);

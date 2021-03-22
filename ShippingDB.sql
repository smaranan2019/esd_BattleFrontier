DROP DATABASE IF EXISTS ShippingDB;
CREATE DATABASE ShippingDB;
use ShippingDB;

create table shipment
(ShipID int not null primary key AUTO_INCREMENT,
PaymentID int not null, 
ShippingStatus varchar(255) not null,
ReceiveStatus varchar(255),
created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table ShippingDetails 
(ShipID int not null primary key,
OrderID int not null,
SellerID int not null,
BuyerID int not null, 
constraint shippingdetails_fk foreign key(ShipID) references shipment(ShipID)
); 

create table Contact
(ShipID int not null primary key,
SellerID int not null, 
BuyerID int not null,
constraint contact_fk foreign key(ShipID) references shipment(ShipID)
);

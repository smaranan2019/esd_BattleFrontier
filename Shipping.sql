create table shipping
(ShipID char(10) not null primary key AUTO_INCREMENT,
Payment_ID char(5) not null,
status_send varchar(255),
status_receive varchar(255),
constraint shipping_fk foreign key(Payment_ID) references payment(Payment_ID)
);


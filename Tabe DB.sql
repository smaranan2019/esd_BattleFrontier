create table payment
(Payment_ID char(5) not null primary key AUTO_INCREMENT, 
order_ID char(5) not null,
status_paid varchar(255),
constraint payment_fk foreign key(order_ID) references order(order_ID)
);
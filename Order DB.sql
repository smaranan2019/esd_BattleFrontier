create table orders
(order_ID char(5) not null primary key AUTO_INCREMENT,
Card_ID char(5) not null,
User_ID varchar(255) not null,
status_appr varchar(255),
constraint order_fk1 foreign key(Card_ID) references card_list(Card_ID),
constraint order_fk2 foreign key(User_ID) references account(User_ID)
);
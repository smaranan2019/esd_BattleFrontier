create table orders
(order_ID int not null primary key AUTO_INCREMENT,
Card_ID int not null,
User_ID int not null,
status_appr varchar(255),
constraint order_fk1 foreign key(Card_ID) references card_list(Card_ID),
constraint order_fk2 foreign key(User_ID) references account(User_ID)
);

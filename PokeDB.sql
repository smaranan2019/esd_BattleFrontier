DROP DATABASE IF EXISTS PokeDB;
CREATE DATABASE PokeDB;
use PokeDB;

create table account
(User_ID varchar(255) not null primary key,
FullName varchar(255) not null,
email varchar(255) not null,
telegram_ID varchar(30) not null,
phone_no char(8) not null,
pswd varchar(255) not null 
);

insert into account values
('GottaCatchEmAll', 'Ash Ketchum', 'ilovepokemon@yahoo.com', 
'@pikapika', '12345678', 'IChooseYou123'),
('ComeGeddit', 'Professor Willow', 'pickme@yahoo.com', 
'@pokeballer', '87654321', 'PickMe123');

create table card_list
(Card_ID char(5) not null primary key,
User_ID varchar(255) not null,
NameOfCard varchar(255),
LevelOfCard int,
TypeOfCard varchar(10),
Price decimal(5,2),
constraint card_list_fk foreign key(User_ID) references account
(User_ID)
);

insert into card_list values
('C0001', 'ComeGeddit', 'Charizard', '240', 'fire', '5.30'),
('C0002', 'ComeGeddit', 'Bulbasaur', '64', 'grass', '1'),
('C0003', 'ComeGeddit', 'Squirtle', '63', 'water', '1');

create table orders
(order_ID int not null primary key AUTO_INCREMENT,
Card_ID char(5) not null,
User_ID varchar(255) not null,
status_appr varchar(255),
constraint order_fk1 foreign key(Card_ID) references card_list
(Card_ID),
constraint order_fk2 foreign key(User_ID) references account
(User_ID)
);

create table payment
(Payment_ID int not null primary key AUTO_INCREMENT, 
order_ID int not null,
status_paid varchar(255),
constraint payment_fk foreign key(order_ID) references orders
(order_ID)
);

create table shipping
(ShipID int not null primary key AUTO_INCREMENT,
Payment_ID int not null,
status_send varchar(255),
status_receive varchar(255),
constraint shipping_fk foreign key(Payment_ID) references payment
(Payment_ID)
);












































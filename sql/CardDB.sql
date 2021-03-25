DROP DATABASE IF EXISTS CardB;
CREATE DATABASE CardDB;
use CardDB;

create table Card_Details
(Card_ID int not null primary key AUTO_INCREMENT,
Pokemon_Name varchar(255),
Pokemon_Type varchar(10),
Image_ID int(10) NOT NULL
);

create table Card_List
(Card_ID int not null primary key,
Seller_ID int not null,
Price decimal(3,2),
constraint Card_List_fk foreign key(Card_ID) references Card_Details(Card_ID)
);

insert into Card_Details (Pokemon_Name, Pokemon_Type) values
('Charizard', 'fire'),
('Bulbasaur', 'grass'),
('Squirtle', 'water'),
('Charmander', 'fire'),
('Caterpie', 'bug'),
('Metapod', 'bug'),
('Wartortle', 'water'),
('Rattata', 'normal'),
('Pidgeot', 'flying'),
('Kakuna', 'Poison'),
('Ivysaur', 'Poison'),
('Butterfree', 'flying');
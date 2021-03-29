DROP DATABASE IF EXISTS AccountDB;
CREATE DATABASE AccountDB;
use AccountDB;

create table account
(User_ID int not null primary key AUTO_INCREMENT,
Username varchar(255) not null,
telehandle varchar(255) not null,
telechat_ID varchar(255) not null default '307267966',
PaypalEmail varchar(255) not null,
password varchar(255) not null 
);

insert into account (Username, telehandle, Paypal_Email, password) values
('AshKetchum', '@pikapika', 'ilovepokemon@yahoo.com', "pikachu"),
('ProfessorWillow', '@pokeballer', 'CardSeller@yahoo.com', "bulbasaur");
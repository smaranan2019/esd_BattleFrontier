DROP DATABASE IF EXISTS accountDB;
CREATE DATABASE accountDB;
use accountDB;

create table account
(User_ID int not null primary key AUTO_INCREMENT,
Username varchar(255) not null,
telehandle varchar(255) not null,
telechat_ID int not null default 307267966,
Paypal_Email varchar(255) not null,
password varchar(255) not null 
);

insert into account (Username, telehandle, Paypal_Email, password) values
('AshKetchum', '@pikapika', 'gotta_ketchum_all@personal.example.com', "pikachu"),
('ProfessorWillow', '@pokeballer', 'CardSeller@yahoo.com', "bulbasaur");
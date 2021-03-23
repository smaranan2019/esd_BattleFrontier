DROP DATABASE IF EXISTS AccountDB;
CREATE DATABASE AccountDB;
use AccountDB;

create table account
(UserID int not null primary key AUTO_INCREMENT,
Username varchar(255) not null,
telehandle varchar(255) not null,
telechatID varchar(255) not null,
PaypalEmail varchar(255) not null 
);

insert into account (Username, telehandle, PaypalEmail) values
('AshKetchum', '@pikapika', 'ilovepokemon@yahoo.com'),
('ProfessorWillow', '@pokeballer', 'CardSeller@yahoo.com');
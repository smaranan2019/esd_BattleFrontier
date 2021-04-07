DROP DATABASE IF EXISTS accountDB;
CREATE DATABASE accountDB;
use accountDB;

create table account
(User_ID int not null primary key AUTO_INCREMENT,
Username varchar(255) not null,
telehandle varchar(255) not null,
telechat_ID varchar(255) not null default "961849285",
Paypal_Email varchar(255) not null,
password varchar(255) not null 
);

insert into account (Username, telehandle, telechat_ID, Paypal_Email, password) values
('Ash Ketchum', '@pikapika', "835159639", 'gotta_ketchum_all@personal.example.com', "pikachu"),
('Professor Oak', '@pokeballer', "37579573", 'sb-n80mu5423090@business.example.com', "oakidokie");

DROP DATABASE IF EXISTS `CardDB`;
CREATE DATABASE IF NOT EXISTS `CardDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use `CardDB`;

create table `Card_Details`
(`Card_ID` int not null primary key AUTO_INCREMENT,
`Pokemon_Name` varchar(255),
`Pokemon_Type` varchar(10),
`Image_path` varchar(255) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table `Card_List`
(`Card_ID` int not null primary key,
`Seller_ID` int not null,
`Price` decimal(4,2) not null,
constraint `Card_List_fk` foreign key(`Card_ID`) references `Card_Details`(`Card_ID`)
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

insert into `Card_Details` (`Pokemon_Name`, `Pokemon_Type`, `Image_path`) values
('Charizard', 'fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_14.png'),
('Bulbasaur', 'grass', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM35/SM35_EN_1.png'),
('Squirtle', 'water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_29.png'),
('Charmander', 'fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_18.png'),
('Caterpie', 'bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_1.png'),
('Metapod', 'bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM10/SM10_EN_3.png'),
('Wartortle', 'water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_24.png'),
('Rattata', 'normal', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM7/SM7_EN_84.png'),
('Pidgeot', 'flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_124.png'),
('Kakuna', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/XY1/XY1_EN_4.png'),
('Ivysaur', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/POP2/POP%20Series%202_EN_7.png'),
('Butterfree', 'flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_3.png');

insert into `Card_List` ( `Card_ID`, `Price`) values
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Charizard'), '40.10'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Bulbasaur'), '10.99'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Squirtle'), '10.99'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Charmander'), '10.99'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Caterpie'), '12.15'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Metapod'), '12.15'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Wartortle'), '25.78'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Rattata'), '10.99'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Pidgeot'), '12.45'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Kakuna'), '12.76'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Ivysaur'), '20.78'),
((select `Card_ID` from `Card_Details` where `Pokemon_Name` = 'Butterfree'), '18.99');


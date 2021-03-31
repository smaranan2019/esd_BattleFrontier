# SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
# SET AUTOCOMMIT = 0;
# START TRANSACTION;
# SET time_zone = "+00:00";

DROP DATABASE IF EXISTS cardDB;
CREATE DATABASE IF NOT EXISTS cardDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use cardDB;

create table card
(card_id int NOT NULL primary key AUTO_INCREMENT,
pokemon_name varchar(255) NOT NULL,
pokemon_type varchar(10) NOT NULL,
image_path varchar(255) NOT NULL
#price decimal(4,2) NOT NULL
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table contact
(card_id int not null primary key,
seller_id int not null,
seller_chat_id int not null,
constraint contact_fk foreign key(card_id) references card(card_id) on delete cascade on update cascade
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*
insert into card (pokemon_name, pokemon_type, image_path, price) values
('Charizard', 'fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_14.png', 40.10),
('Bulbasaur', 'grass', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM35/SM35_EN_1.png', 10.99),
('Squirtle', 'water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_29.png', 10.99),
('Charmander', 'fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_18.png', 10.99),
('Caterpie', 'bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_1.png', 12.15),
('Metapod', 'bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM10/SM10_EN_3.png', 12.15),
('Wartortle', 'water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_24.png', 25.78),
('Rattata', 'normal', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM7/SM7_EN_84.png', 10.99),
('Pidgeot', 'flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_124.png', 12.45),
('Kakuna', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/XY1/XY1_EN_4.png', 12.76),
('Ivysaur', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/POP2/POP%20Series%202_EN_7.png', 20.78),
('Butterfree', 'flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_3.png', 18.99);
*/
insert into card (pokemon_name, pokemon_type, image_path) values
('Charizard', 'Fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_14.png'),
('Bulbasaur', 'Grass', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM35/SM35_EN_1.png'),
('Squirtle', 'Water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_29.png'),
('Charmander', 'Fire', 'https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_18.png'),
('Caterpie', 'Bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_1.png'),
('Metapod', 'Bug', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM10/SM10_EN_3.png'),
('Wartortle', 'Water', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_24.png'),
('Rattata', 'Normal', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM7/SM7_EN_84.png'),
('Pidgeot', 'Flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM9/SM9_EN_124.png'),
('Kakuna', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/XY1/XY1_EN_4.png'),
('Ivysaur', 'Poison', 'https://assets.pokemon.com/assets/cms2/img/cards/web/POP2/POP%20Series%202_EN_7.png'),
('Butterfree', 'Flying', 'https://assets.pokemon.com/assets/cms2/img/cards/web/SM1/SM1_EN_3.png');

insert into contact (card_id, seller_id, seller_chat_id) values
((select card_id from card where pokemon_name='Charizard'), 2, '307267966'),
((select card_id from card where pokemon_name='Bulbasaur'), 2, '307267966'),
((select card_id from card where pokemon_name='Squirtle'), 2, '307267966'),
((select card_id from card where pokemon_name='Charmander'), 2, '307267966'),
((select card_id from card where pokemon_name='Caterpie'), 2, '307267966'),
((select card_id from card where pokemon_name='Metapod'), 2, '307267966'),
((select card_id from card where pokemon_name='Wartortle'), 2, '307267966'),
((select card_id from card where pokemon_name='Rattata'), 2, '307267966'),
((select card_id from card where pokemon_name='Pidgeot'), 2, '307267966'),
((select card_id from card where pokemon_name='Kakuna'), 2, '307267966'),
((select card_id from card where pokemon_name='Ivysaur'), 2, '307267966'),
((select card_id from card where pokemon_name='Butterfree'), 2, '307267966');

select * from `card`;

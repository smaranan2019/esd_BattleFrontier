DROP DATABASE IF EXISTS CardB;
CREATE DATABASE CardDB;
use CardDB;

create table CardDetails
(CardID int not null primary key AUTO_INCREMENT,
PokemonName varchar(255),
PokemonType varchar(10),
ImageID int(10) NOT NULL
);

create table CardList
(CardID int not null primary key,
SellerID int not null,
Price decimal(3,2),
constraint CardListfk foreign key(CardID) references CardDetails(CardID)
);

insert into CardDetails (PokemonName, PokemonType) values
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
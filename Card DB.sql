create table card_list
(Card_ID char(5) not null primary key,
User_ID varchar(255) not null,
NameOfCard varchar(255),
LevelOfCard int,
TypeOfCard varchar(10),
Price decimal(5,2),
constraint card_list_fk foreign key(User_ID) references account(User_ID)
);

insert into card_list values
('C0001', 'ComeGeddit', 'Charizard', '240', 'fire', '5.30'),
('C0002', 'ComeGeddit', 'Bulbasaur', '64', 'grass', '1'),
('C0003', 'ComeGeddit', 'Squirtle', '63', 'water', '1');
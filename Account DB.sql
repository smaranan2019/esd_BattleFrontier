create table account
(User_ID varchar(255) not null primary key,
FullName varchar(255) not null,
email varchar(255) not null,
telegram_ID varchar(30) not null,
phone_no char(8) not null,
pswd varchar(255) not null 
);

insert into account values
('GottaCatchEmAll', 'Ash Ketchum', 'ilovepokemon@yahoo.com', '@pikapika', '12345678', 'IChooseYou123'),
('ComeGeddit', 'Professor Willow', 'pickme@yahoo.com', '@pokeballer', '87654321', 'PickMe123');









CREATE DATABASE user_gamer;

use user_gamer;

CREATE TABLE cadastrar(
 id_usuario INT primary key auto_increment,
 nome VARCHAR(50) ,
 email VARCHAR(60) ,
 senha VARCHAR(6)
);

CREATE TABLE games (
    id_game INT PRIMARY KEY auto_increment,
    slug varchar (200) not null,
    comment VARCHAR(300) NOT NULL,
    rating int not null,
    sentiment varchar(50)
);






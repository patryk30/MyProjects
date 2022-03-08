-- tworzenia bazy i zapytania SQL INSERT/UPDATE

USE master
GO

if exists(select * from sysdatabases where name = 'Streaming_platform')
	drop database Streaming_platform
GO

CREATE DATABASE Streaming_platform
GO

USE Streaming_platform
GO

--tabela z gatunkami--
CREATE TABLE Genres(
	Genre_id	INT NOT NULL PRIMARY KEY,
	Name		nchar(50) NOT NULL 
)

--tabela z uzytkownikami, zakladamy ze uzytkownicy musza podac date urodzenia--
CREATE TABLE Users(
	User_id		INT NOT NULL PRIMARY KEY,
	Nick		nchar(50) NOT NULL UNIQUE,
	Email		nchar(100) NOT NULL,
	Birth_date	DATE NOT NULL,
	CONSTRAINT Birth_date CHECK (Birth_Date < getdate()),
	Gender		BIT NULL		
)

--tabela z kanalami--
-- zakladamy, ze prowadzacy kanaly musza tez podac imie i nazwisko oraz sa tez zwyklymi uzytkownikami
CREATE TABLE Channels(
	Channel_id	INT NOT NULL PRIMARY KEY,
	Channel_name nchar(50) NOT NULL UNIQUE,
	Name		nchar(50) NOT NULL,
	Surname		nchar(100) NOT NULL,
	User_id		INT NOT NULL REFERENCES Users(User_id),
	Country		nchar(50) NULL,
)

---obserwowane kanaly--
CREATE TABLE Users_channels(
	User_id		INT NOT NULL REFERENCES Users(User_id),
	Channel_id		INT NOT NULL REFERENCES Channels(Channel_id),
	PRIMARY KEY(User_id, Channel_id)
)

-- tabela z filmami--
CREATE TABLE Movies(
	Movie_id	INT NOT NULL PRIMARY KEY,
	Title		nchar(50) NOT NULL,
	Length		TIME NOT NULL,
--	Genre_id	INT NOT NULL REFERENCES Genres(Genre_id),
	Premiere_date	DATE NOT NULL,
	Maker_id	INT NOT NULL REFERENCES Channels(Channel_id),
	Production_country nchar(50) NOT NULL
)

-- tabela z filmami i ich gatunkami
CREATE TABLE Movie_genres(
	Movie_id	INT NOT NULL REFERENCES Movies(Movie_id),
	Genre_id	INT NOT NULL REFERENCES Genres(Genre_id),
	PRIMARY KEY(Movie_id, Genre_id)
)

--Historia ogladania (uzytkownik moze obejrzec ten sam film kilkukrotnie)--
CREATE TABLE History_watch(
	Watch_id	INT NOT NULL PRIMARY KEY,
	User_id		INT NOT NULL REFERENCES Users(User_id),
	Movie_id	INT NOT NULL REFERENCES Movies(Movie_id),
	Date_play	DATETIME NOT NULL,
--	PRIMARY KEY(User_id, Movie_id)
)


-- ------------------------------------------------------------------------------------------------
-- Zadanie 2 --


GO
INSERT INTO Genres VALUES(1, 'Action film')
INSERT INTO Genres Values(2, 'Fantasy')
INSERT INTO Genres Values(3, 'Animated film')
INSERT INTO Genres Values(4, 'Comedy')
INSERT INTO Genres Values(5, 'Horror')
INSERT INTO Genres Values(6, 'Melodrama')
INSERT INTO Genres Values(7, 'Science fiction')
INSERT INTO Genres Values(8, 'Adventure film')
INSERT INTO Genres Values(9, 'Thriller')
INSERT INTO Genres Values(10, 'Romantic comedy')
INSERT INTO Genres Values(11, 'Drama')
INSERT INTO Genres Values(12, 'Comedy drama')
INSERT INTO Genres Values(13, 'Documentary')
GO



GO 
INSERT INTO Users VALUES(1, 'moviefreak123', 'ghost.movie@gmail.com', '1998-11-12', 1)
INSERT INTO Users (User_id,Nick,Email,Birth_date) VALUES(2, 'hello123', 'sisters888y@gmail.com', '2003-12-13')
INSERT INTO Users VALUES(3, 'wannapassdatabases1', 'sandra.bowie@gmail.com', '1999-08-07', 0)
INSERT INTO Users VALUES(4, 'patrick567', 'patrick.brady@gmail.com', '1957-03-17', 1)
INSERT INTO Users VALUES(5, 'amanda2308', 'amanda.sand@gmail.com', '2000-06-27', 0)
INSERT INTO Users VALUES(6, 'martinmovies', 'martin.kow145@gmail.com', '2002-02-16', 1)
INSERT INTO Users VALUES(7, 'frankbestdirector', 'frank.darabont@gmail.com', '1959-01-28', 1)
INSERT INTO Users VALUES(8, 'olivieroscars', 'olivier.nakache@gmail.com', '1973-04-15', 1)
INSERT INTO Users VALUES(9, 'fordfrancais', 'francis.coppola@gmail.com', '1939-04-07', 1)
INSERT INTO Users VALUES(10, 'jackson111', 'peter.jackson@gmail.com', '1961-11-30', 1)
GO

GO
INSERT INTO Channels VALUES(1, 'bestmovies', 'Martin', 'Kowalsky', 6, 'Poland')
INSERT INTO Channels VALUES(2, 'lordofthering', 'Peter', 'Jackson', 10, 'New Zealand')
INSERT INTO Channels VALUES(3, 'arsenelupin', 'Antoine', 'Lupin', 1, 'France')
INSERT INTO Channels VALUES(4, 'famousfrench', 'Frank', 'Darabont', 7, 'France')
INSERT INTO Channels VALUES(5, 'bestdirector', 'Francis', 'Coppola', 9, 'USA')
INSERT INTO Channels VALUES(6, 'famousmovies', 'Olivier', 'Nakache', 8, 'France')
GO

GO
INSERT INTO Users_channels VALUES(1,2)
INSERT INTO Users_channels VALUES(2,1)
INSERT INTO Users_channels VALUES(2,2)
INSERT INTO Users_channels VALUES(3,1)
INSERT INTO Users_channels VALUES(4,1)
INSERT INTO Users_channels VALUES(4,2)
INSERT INTO Users_channels VALUES(5,1)
INSERT INTO Users_channels VALUES(5,2)
INSERT INTO Users_channels VALUES(6,2)
INSERT INTO Users_channels VALUES(6,3)
INSERT INTO Users_channels VALUES(3,5)
GO

GO
INSERT INTO Movies VALUES (1,'The Shawshank Redemption','02:22:00','1994-09-10',4, 'USA')
INSERT INTO Movies VALUES (2,'Intouchables','02:22:00','2011-09-23',6, 'France')
INSERT INTO Movies VALUES (3,'The Godfather I','02:55:00','1972-03-15',5, 'USA')
INSERT INTO Movies VALUES (4,'The Godfather II','03:20:00','1974-12-12',5, 'USA')
INSERT INTO Movies VALUES (5,'The Godfather III','02:42:00','1990-12-20',5, 'USA')
INSERT INTO Movies VALUES (6,'The Lord of the Rings: The Return of the King','03:21:00','2003-12-05',2, 'New Zealand')
GO

GO
INSERT INTO History_watch VALUES(1,1,1,'2020-01-22 04:35:27.000')
INSERT INTO History_watch VALUES(2,6,3,'2019-11-25 03:32:21.000')
INSERT INTO History_watch VALUES(3,6,4,'2019-11-26 18:12:21.000')
INSERT INTO History_watch VALUES(4,6,6,'2021-07-08 00:35:22.000')
INSERT INTO History_watch VALUES(5,2,3,'2019-04-01 19:44:27.000')
INSERT INTO History_watch VALUES(6,2,2,'2018-05-22 00:35:37.000')
INSERT INTO History_watch VALUES(7,2,5,'2020-06-07 15:41:27.000')
INSERT INTO History_watch VALUES(8,2,6,'2020-03-09 16:17:17.000')
INSERT INTO History_watch VALUES(9,1,5,'2020-01-13 17:35:27.000')
INSERT INTO History_watch VALUES(10,3,5,'2021-09-07 00:35:27.000')
INSERT INTO History_watch VALUES(11,3,2,'2021-08-29 19:35:37.000')
INSERT INTO History_watch VALUES(12,3,4,'2021-09-30 21:05:27.000')
INSERT INTO History_watch VALUES(13,4,5,'2019-10-03 18:15:27.000')
INSERT INTO History_watch VALUES(14,7,5,'2019-11-06 17:35:37.000')
INSERT INTO History_watch VALUES(15,5,5,'2018-10-16 15:35:23.000')
INSERT INTO History_watch VALUES(16,5,3,'2019-07-19 15:25:27.000')
INSERT INTO History_watch VALUES(17,4,1,'2018-01-14 03:45:17.000')
INSERT INTO History_watch VALUES(18,5,4,'2021-02-04 23:05:27.000')
INSERT INTO History_watch VALUES(19,5,4,'2021-02-07 23:25:27.000')
INSERT INTO History_watch VALUES(20,6,5,'2021-02-28 12:15:27.000')
INSERT INTO History_watch VALUES(21,9,5,'2020-12-31 02:15:27.000')
INSERT INTO History_watch VALUES(22,1,2,'2020-12-06 07:15:27.000')
INSERT INTO History_watch VALUES(23,4,6,'2019-09-24 05:35:27.000')
INSERT INTO History_watch VALUES(24,8,6,'2018-04-17 03:35:27.000')
INSERT INTO History_watch VALUES(25,1,6,'2019-06-08 01:28:27.000')
GO

GO
INSERT INTO Movie_genres VALUES(1,11)
INSERT INTO Movie_genres VALUES(2,12)
INSERT INTO Movie_genres VALUES(3,11)
INSERT INTO Movie_genres VALUES(4,11)
INSERT INTO Movie_genres VALUES(5,11)
INSERT INTO Movie_genres VALUES(6,2)
GO

-- modyfikowanie rekordow w tabeli History_watch
UPDATE History_watch
SET Date_play = CASE WHEN User_id IN (SELECT User_id FROM History_watch WHERE User_id=5) THEN DATEADD(hh, -1, Date_play) ELSE Date_play END;
-- lacznie 4 rekordy zmodyfikowane, reszta taka sama

UPDATE History_watch
SET Date_play = '2018-04-17 13:35:27.000' WHERE User_id=8 AND Movie_id=6
--jeden rekord zmodyfikowany


-- Indeksy
-- dla kluczy glownych indeksy sa tworzone  automatycznie

--kolumny o unikalnych wartosciach (default - NONCLUSTERED)
CREATE UNIQUE INDEX chname ON Channels(Channel_name)
CREATE UNIQUE INDEX usernick ON Users(Nick)
CREATE UNIQUE INDEX genrename ON Genres(Name)

--kolumny potencjalnie czesto uzywane przy poleceniach sql (JOIN, EXISTS, IN)
CREATE INDEX hismovies ON History_watch(Movie_id)
CREATE INDEX hisuser ON History_watch(User_id) 
CREATE INDEX hisdate ON History_watch(Date_play)
CREATE INDEX moviemaker ON Channels(Name, Surname) 

CREATE INDEX movmaker ON Movies(Maker_id)
CREATE INDEX movcountry ON Movies(Production_country)


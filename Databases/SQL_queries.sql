-- Zadanie 4 ---> SQL SELECT
USE Streaming_platform
GO

--- podpunkt 1
SELECT u.Nick,
	sum( DATEPART(SECOND, m.Length)/60 + 
		DATEPART(MINUTE, m.Length) + 
		60 * DATEPART(HOUR, m.Length) 
		) as 'Total minutes watched',
	ch.Channel_name
FROM History_watch h
JOIN Users u ON h.User_id = u.User_id
JOIN Movies m ON h.Movie_id = m.Movie_id
JOIN Channels ch ON ch.Channel_id = m.Maker_id
GROUP BY ch.Channel_name , u.Nick



------------------------------------------------------------------------------------
-- podpunkt 2
SELECT
	u.Nick AS User_nickname,
	ch.Channel_name,
	help.Films_watched
FROM Users u
JOIN (SELECT Maker_id,
	User_id, 
	COUNT(User_id) AS Films_watched
	FROM (SELECT DISTINCT User_id, Maker_id, m.Movie_id 
	FROM History_watch h 
	JOIN Movies m ON h.Movie_id = m.Movie_id) AS Movies_distinct
	GROUP BY Maker_id, User_id
	HAVING COUNT(User_id) <3 ) help
ON help.User_id = u.User_id
JOIN Users_channels uch ON help.Maker_id = uch.Channel_id AND help.User_id = uch.User_id
JOIN Channels ch ON ch.Channel_id = uch.Channel_id


---------------------------------------------------------------------------
-- podpunkt 3
SELECT 
	Name AS Genre,
	Title AS Movie_title,
	Views_number
FROM (SELECT 
		Name,
		Title,
		Views_number,
		MAX(Views_number) OVER (PARTITION BY Name) AS help_var
	FROM (SELECT 
			g.Name,
			m.Title,
			COUNT(*) AS Views_number
		FROM History_watch h
		JOIN Movies m ON h.Movie_id = m.Movie_id
		JOIN Movie_genres mg ON mg.Movie_id = m.Movie_id
		JOIN Genres g ON g.Genre_id = mg.Genre_id
		GROUP BY g.Name, m.Title) help1 
		) help2
WHERE Views_number = help_var


---------------------------------------------------------------------------------------------
-- Podpunkt 4
SELECT Channel_name,
	ROUND(CONVERT(DECIMAL(4,2),help1.Viewings)/help2.Movies_produced, 2) AS Viewings_per_movie 
FROM Channels ch
JOIN (SELECT Channel_id,
		COUNT(*) AS Viewings
	FROM History_watch h
	JOIN Movies m ON h.Movie_id = m.Movie_id
	JOIN Channels ch ON ch.Channel_id = m.Maker_id
	GROUP BY Channel_id) help1
ON ch.Channel_id = help1.Channel_id
JOIN (SELECT Maker_id,
		COUNT(*) AS Movies_produced
		FROM Movies
		GROUP BY Maker_id) help2
ON ch.Channel_id = help2.Maker_id
ORDER BY Viewings_per_movie DESC;


---------------------------------------------------------------------
-- Podpunkt 5
CREATE VIEW Subscriptions AS (
	SELECT Channel_id, COUNT(*) AS sub
	FROM Users_channels
	GROUP BY Channel_id);

SELECT Title AS Movies
FROM Movies
WHERE Maker_id IN (SELECT Channel_id
					FROM Subscriptions
					WHERE sub = (SELECT TOP 1 sub
								FROM Subscriptions
								ORDER BY sub DESC))



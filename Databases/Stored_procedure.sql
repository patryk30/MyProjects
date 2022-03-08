-- 2.5 procedura sk³adowana

USE Streaming_platform
GO 

if OBJECT_ID('HistoryArchive') IS NOT NULL  drop table HistoryArchive ;

-- Stworzona przeze mnie tabela z histori¹ ogl¹dania filmów ma nazwê 'History_watch'
	SELECT * INTO HistoryArchive FROM History_watch WHERE 0=1;
	SELECT * FROM HistoryArchive

	Alter table HistoryArchive
		ADD CONSTRAINT  [FK_Users] FOREIGN KEY ( User_id ) REFERENCES Users(User_id),
		CONSTRAINT [FK_Movies] FOREIGN KEY ( Movie_id ) REFERENCES Movies(Movie_id),
		CONSTRAINT [PK_watch] PRIMARY KEY (Watch_id);


	Alter table Movies
	ADD ViewsCnt INT DEFAULT 0 WITH VALUES
	

select * from Movies
select * from History_watch
select * from HistoryArchive


IF OBJECT_ID('history_to_archive') IS NOT NULL 
	DROP PROC history_to_archive;
GO

CREATE PROCEDURE history_to_archive 
	@DaysCount int
AS
BEGIN
	
	DECLARE @CurrentDate DATETIME 
	DECLARE @Archivedate DATETIME
	DECLARE @archivedIDs TABLE(User_id int, Movie_id int);

	SET @CurrentDate = GETDATE()

	IF (SELECT COUNT(*) FROM History_watch 
		WHERE DATEDIFF(day, @CurrentDate, Date_play) <= @DaysCount) = 0
	BEGIN
		PRINT 'There are no records to archive';
		RETURN;
	END;

	SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
	
	BEGIN TRANSACTION 
	BEGIN TRY
		
		PRINT @CurrentDate;
		PRINT @DaysCount;

		INSERT INTO HistoryArchive
		OUTPUT INSERTED.User_id, INSERTED.Movie_id INTO @archivedIDs
		SELECT * FROM History_watch WHERE DATEDIFF(day, Date_play, @CurrentDate) > @DaysCount;

		UPDATE Movies
		SET ViewsCnt = (SELECT ViewsCnt + Views_new
						FROM (SELECT Movie_id, COUNT(*) AS Views_new
								FROM @archivedIDs
								GROUP BY Movie_id) help
						WHERE help.Movie_id = Movies.Movie_id)

		DELETE FROM History_watch
		FROM History_watch h
		JOIN @archivedIDs ar ON h.User_id = ar.User_id AND h.Movie_id = ar.Movie_id;

	COMMIT TRANSACTION
	END TRY

	BEGIN CATCH
		ROLLBACK TRANSACTION 
	END CATCH
END

EXECUTE history_to_archive 476

--zapytania do testu poprawnosci
SELECT DATEADD(DAY, -476, getdate())

SELECT Movie_id, 
	COUNT(*) AS ViewsCnt
FROM HistoryArchive
GROUP BY Movie_id
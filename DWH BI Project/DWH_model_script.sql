USE master
GO

if exists(select * from sysdatabases where name = 'ErgastF1_DWH')
	drop database ErgastF1_DWH
GO

CREATE DATABASE ErgastF1_DWH
GO

USE ErgastF1_DWH
GO


-- Fact table

CREATE TABLE [dbo].[ResultsFact] (
  NewResultId int IDENTITY(1,1) NOT NULL,
  ResultId int NOT NULL,
  RaceId int NOT NULL,
  DriverId int NOT NULL,
  ConstructorId int NOT NULL,
  Number int NOT NULL,
  Grid int NOT NULL,
  Position int NOT NULL,
  DriverPoints float NOT NULL,
  Laps int NOT NULL, 
  [Time] varchar(255) NOT NULL,
  Milliseconds int NOT NULL,
  FastestLap int NOT NULL, 
  [Rank] int NOT NULL,
  FastestLapTime varchar(255) NOT NULL,
  FastestLapSpeed varchar(255) NOT NULL, 
  DateId int NOT NULL,
  Qual1_Time varchar(255) NOT NULL,
  Qual2_Time varchar(255) NOT NULL,
  Qual3_Time varchar(255) NOT NULL,
  QualPosition int NOT NULL,
  [Status] varchar(255) NOT NULL,
  Temperature decimal(18,1) NOT NULL,	
  Wind_speed decimal(18,1) NOT NULL,
  Wind_direction decimal(18,1) NOT NULL,
  Cloudiness decimal(18,1) NOT NULL,	
  Humidity decimal(18,2) NOT NULL,
  Air_pressure decimal(18,1) NOT NULL,
  Precipitation decimal(18,2) NOT NULL,
  PRIMARY KEY (NewResultId)
  );





-- dimension tables

CREATE TABLE [dbo].[ConstructorsDimension] (  
  ConstructorId int NOT NULL,
  ConstructorRef varchar(255) NOT NULL,
  [Name] varchar(255) NOT NULL,
  Nationality varchar(255) NOT NULL,
  PRIMARY KEY (ConstructorId)
);


--join races and circuits table
CREATE TABLE [dbo].[RacesDimension] (
  RaceId int NOT NULL,
  [Round] int NOT NULL,
  CircuitId int NOT NULL,
  [RaceName] varchar(255) NOT NULL,
  RaceDateId int NOT NULL,
  RaceTime time NOT NULL,
  CircuitName varchar(255) NOT NULL,
  [Location] varchar(255) NOT NULL,
  Country varchar(255) NOT NULL,
  Lattitude float NOT NULL,
  Longitude float NOT NULL,
  Altitude int NOT NULL,
  PRIMARY KEY (RaceId)
);



SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DateDimension](
	[DateID] [int] NOT NULL,
	[Date] [date] NOT NULL,
	[Day] [tinyint] NOT NULL,
	[DaySuffix] [char](2) NOT NULL,
	[Weekday] [tinyint] NOT NULL,
	[WeekDayName] [varchar](10) NOT NULL,
	[IsWeekend] [bit] NOT NULL,
	[IsHoliday] [bit] NOT NULL,
	[HolidayText] [varchar](64) SPARSE  NULL,
	[DOWInMonth] [tinyint] NOT NULL,
	[DayOfYear] [smallint] NOT NULL,
	[WeekOfMonth] [tinyint] NOT NULL,
	[WeekOfYear] [tinyint] NOT NULL,
	[ISOWeekOfYear] [tinyint] NOT NULL,
	[Month] [tinyint] NOT NULL,
	[MonthName] [varchar](10) NOT NULL,
	[Quarter] [tinyint] NOT NULL,
	[QuarterName] [varchar](6) NOT NULL,
	[Year] [int] NOT NULL,
	[MMYYYY] [char](6) NOT NULL,
	[MonthYear] [char](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[DateID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TYPE [dbo].[Flag] FROM [char](3) NOT NULL
GO

CREATE TABLE [dbo].[DriversDimension] (
  DriverId int IDENTITY(1,1) NOT NULL,
  OriginalDriverId int not null,
  DriverRef varchar(255) NOT NULL,
  Number int NOT NULL,
  Code varchar(10) NOT NULL,
  Forename varchar(255) NOT NULL,
  Surname varchar(255) NOT NULL,
  FullName nvarchar(80) not null,
  BirthDate int NOT NULL,
  Nationality varchar(255) NOT NULL,
  ValidFrom datetime not null,
  ValidTo datetime not null,
  Active [dbo].[Flag] not null
  PRIMARY KEY (DriverId)
);



ALTER TABLE [dbo].[ResultsFact]  WITH CHECK ADD FOREIGN KEY([DriverId])
REFERENCES [dbo].[DriversDimension] ([DriverId])
GO

ALTER TABLE [dbo].[ResultsFact]  WITH CHECK ADD FOREIGN KEY([RaceId])
REFERENCES [dbo].[RacesDimension] ([RaceId])
GO

ALTER TABLE [dbo].[ResultsFact]  WITH CHECK ADD FOREIGN KEY([ConstructorId])
REFERENCES [dbo].[ConstructorsDimension] ([ConstructorId])
GO

ALTER TABLE [dbo].[ResultsFact]  WITH CHECK ADD FOREIGN KEY([DateId])
REFERENCES [dbo].[DateDimension] ([DateID])
GO

ALTER TABLE [dbo].[DriversDimension]  WITH CHECK ADD FOREIGN KEY([BirthDate])
REFERENCES [dbo].[DateDimension] ([DateID])
GO

ALTER TABLE [dbo].[RacesDimension]  WITH CHECK ADD FOREIGN KEY([RaceDateId])
REFERENCES [dbo].[DateDimension] ([DateID])
GO




-- Staging table
CREATE TABLE [dbo].[ResultsFactStaging] (
  ResultId int NOT NULL,
  RaceId int NOT NULL,
  DriverId int NOT NULL,
  ConstructorId int NOT NULL,
  Number int NULL,
  Grid int NOT NULL,
  Position int NULL, 
  DriverPoints float NULL,
  Laps int NULL,
  [Time] varchar(255) NULL,
  Milliseconds int NULL,
  FastestLap int NULL,
  [Rank] int NULL,
  FastestLapTime varchar(255)  NULL, 
  FastestLapSpeed varchar(255)  NULL, 
  Date [date]  NULL,
  Qual1_Time varchar(255)  NULL,
  Qual2_Time varchar(255)  NULL,
  Qual3_Time varchar(255)  NULL,
  QualPosition int  NULL,
  [Status] varchar(255)  NULL,
  Temperature varchar(50) NULL,		
  Wind_speed varchar(50) NULL,		
  Wind_direction varchar(50) NULL,
  Cloudiness varchar(50) NULL,			
  Humidity varchar(50) NULL,			
  Air_pressure varchar(50) NULL,			
  Precipitation varchar(50) NULL
);
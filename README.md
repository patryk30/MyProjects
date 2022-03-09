# My Projects
In this repository I include the most interesting projects I've done during my studies. 

## 1. Databases project
Working environment: Microsoft SQL Server Management Studio 2018

The main aim of the project was to design relational database for the streaming platform which offers access to thousands of movies. Main points of the project:
  * Tables creation by SQL code.
  * Introducing indexes in order to improve SQL query performance.
  * Writing several SQl SELECT queries to prepare some reports.
  * Preparation of Stored Procedure due to which records with movie viewings older than definded time period are moved to the archive table.

Detailed project description and report in Polish are in seperate files in 'Databases' folder.

## 2. Cluster analysis
Working environment: Python - Jupyter notebook, Spyder 

The aim of the project was to test the performance of different clusterisations on downloaded and original benchmark sets. Methods used:
  * *K-means* method
  * Hierarchical clustering i.e.
    - single linkage
    - ward linkage
    - complete linkage
    - average linkage
  * Spectral algorithm - implemented by myself
  * DBSCAN algorithm
  * Genie algorithm

The effectiveness of the methods was compared using *Fowlkes-Mallows index* and *Adjusted Rand index*. The results were visualised on the 2 or 3-dimensional graphs (if dimensions of the datasets weren't greater than 3). 

## 3. Social Diagnosis - Data Visualisation
Working environment: RStudio (R programming language, R Markdown)

The project was devoted to the subject of Social Diagnosis from years 2000-2015 (http://www.diagnoza.com/), its aim being to prepare a report which would analyse the research questions posed. Graphs were generated mainly using **dplyr** and **ggplot2** libraries. They show distribution of answers for different questions according to the allocation of respondents to a BMI group (BMI indices were categorized during preprocessing). The report was written using R Markdown and then generated as .pdf file.

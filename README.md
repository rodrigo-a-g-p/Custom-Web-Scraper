# Custom Web Scraper - Top 20 All-Time Goalscorers

This project consists of a web scraping script that retrieves the top 20 goalscorers of all-time of a given football competition, as well as associated statistics, according to the database of zerozero.pt

![Alt text](images/zerozero-logo.png)

zerozero.pt is a portuguese website specialized in football news and statistics.

This script takes in a URL that points towards a given zerozero.pt page that includes a table of statistics, scrapes the data, and converts the table into a csv file.

In this script I decided to go only for the top 20 entries in each table for simplicity purposes, as adding more entries would mean changing web pages.

I decided to scrape the data from three different football competitions: The UEFA Champions League, the FIFA World cup, and the English Premier League.

This script can be applied only to tables from zerozero.pt that follow the same column structure as the tables of the competitions mentioned above. These include tables of all-time goalscorers from other competitions. The data itself can be scraped from any table. However, for tables that do not follow the same column structure, the column names will not be assigned properly, rendering the final output file redundant. Other errors may occur as a result of different column structures of the scraped tables.   

In the output files, the players are ranked by number of goals scored in the competition in question.

As more matches are played and added to the database, the output files will change over time.

Special thanks to the zerozero.pt team for creating an awesome website.



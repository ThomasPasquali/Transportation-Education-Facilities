# Code libraries

This directory stores all he code libraries developded and/or adopted to collect project resources.

Files are structured:

## Flixbus and Trenitalia

Folders contain JavaScript scripts used to test the respective APIs (WITHOUT SUCCESS!).

## E656 scraper

To scrape FTM *Routes* and *Trips*, from `Code Libraries/E656_scraper` run:
```bash
scrapy crawl FTMTrains -O ftm_routes_trips.json
```

To scrape FTM *Stops*, from `Code Libraries/E656_scraper` (Wikipedia) run:
```bash
scrapy crawl FTMStops -O ftm_stops.json
```

To scrape *Trento station trains*, from `Code Libraries/E656_scraper` run:
```bash
scrapy crawl Trains -O trento_trains.json
```

To scrape *train stops*, from `Code Libraries/E656_scraper` run:
```bash
scrapy crawl Stops -O stops.json
```

**Note**: data needs to be leater cleaned and converted to GTFS.

## Common transportation data parser

`0_scraped_transport.py` is a Python script that transformed the `json` results of the scraping into GTFS datasets.

`1_transport.py` is a Python script that parser and cleans data from GTFS compliant files. These files can be found in the directory `Raw data` and are divided in subfolders depending on the provider, region and urban/extraurban.

The idea is that the GTFS notebook will be responsible to merge all datasets, therefore, running all the code cells inside will populate the folder `Persed data` with the final datasets obtained by processing and merging different sources data.

`2_edu.py` is a Python script that completes, parses and unifies data regarding educational facilities.

`3_users.py` is a Python script that transforms the "raw" end users info into datasets compatible with the knowledge layer.

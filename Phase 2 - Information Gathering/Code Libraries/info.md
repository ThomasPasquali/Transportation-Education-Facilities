# Code libraries

This directory stores all he code libraries developded and/or adopted to collect project resources.

Files are structured:

## Flixbus and Trenitalia

Folders contain JavaScript scripts used to test the respective APIs (WITHOUT SUCCESS!).

## E656 scraper

To scrap FTM *Routes* and *Trips*, from `Code Libraries/E656_scraper` run:
```bash
scrapy crawl FTMTrains -O ftm_routes_trips.json
```

To scrap FTM *Stops*, from `Code Libraries/E656_scraper` run:
```bash
scrapy crawl FTMStops -O ftm_stops.json
```

**Note**: data needs to be leater cleaned and converted to GTFS.

## Common transportation data parser

`parser.ipynb` is a Jupiter Notebook that parser and cleans data from GTFS compliant files. These files can be found in the directory `Raw data` and are divided in subfolders depending on the provider, region and urban/extraurban.

The idea is that the GTFS notebook will be responsible to merge all datasets, therefore, running all the code cells inside will populate the folder `Persed data` with the final datasets obtained by processing and merging different sources data.

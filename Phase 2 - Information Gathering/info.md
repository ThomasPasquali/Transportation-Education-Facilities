# Information gathering

In this directory you have store all the material (resources included) considered for the information gathering phase

This folder is structured as follows:
- **Code libraries** contains all the necessary scripts to obtain the final datasets from the "raw data" (please refer to its `info.md` file);
- **TTL files** contains all the *formal* schemas for the final KG (edited with Protege);
- **Karma models** contains all the files that can be imported with Karma to automatically link data to schemas;
- **Parsed data** will be the destination folder for the final datasets;
- **Raw data** contains all the "static" data that will be used to produce the final datasets;

In order to produce the final csv datasets in `Parsed data` please run the following commands:
```bash
cd Code\ Libraries/E656_scraper/

# Scraping (for more details refer to "Code Libraries/info.md")
scrapy crawl FTMTrains -O ftm_routes_trips.json
scrapy crawl FTMStops -O ftm_stops.json
scrapy crawl Trains -O trento_trains.json
scrapy crawl Stops -O stops.json

cd ..

# Run all code cells in the notebook
jupyter nbconvert --to notebook --inplace --execute parser.ipynb
```

# Code libraries

This directory stores all he code libraries developded and/or adopted to collect project resources.

Files are structures in folders:

- **Flixbus** and **Trenitalia** folders contain JavaScript scripts that allow to retreive information from the respective APIs.
- **Trentino Trasporti** contains a Jupiter Notebook that parser and cleans data from GTFS compliant files. These files can be found in the directory `Raw data` and are divided in two subfolders, one for urban busses and one for extraurban.

The idea is that the GTFS notebook will be responsible to merge all datasets, therefore, running all the code cells inside will populate the folder `Persed data` with the final datasets obtained by processing and merging different sources data.

# Data Definiton

In this phase, the final datasets have been linked to the knowledge layer. Since some files are too big for GitHub, they have been uploaded to Google Drive:
- Datasets: [https://drive.google.com/drive/folders/1PUmhXYnM5fd-TqePUDAumem9luqa6qcv?usp=sharing](https://drive.google.com/drive/folders/1PUmhXYnM5fd-TqePUDAumem9luqa6qcv?usp=sharing)
- Karma TTL datases [https://drive.google.com/drive/folders/166Gq2JADO7hJCPuWrOsYg5kZOM5eDim6?usp=sharing](https://drive.google.com/drive/folders/166Gq2JADO7hJCPuWrOsYg5kZOM5eDim6?usp=sharing)

To obtain the final KG file please download the files in `Karma TTL datases` and put them in the folder `Karma RDF` and then run from this folder:

```bash
python3 generate_KG.py
```

This command will create a file `KG.ttl` containing all rdf datasets.

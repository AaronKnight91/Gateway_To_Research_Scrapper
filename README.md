# Gateway to Research Scrapper

To run the scrapper, run the following command on the command line:
```
python run.py
```
This script can also take an argument to select the output file the data is saved to.
To select which file the data is saved to, use the following command:
```
python run.py --output <output_file.csv>
```
To check if all projects have been correctly scrapped, download the csv of projects from Gateway to Research and save it in the gtr project folder.
Ensure that the csv is call projectsearch.csv. Then run the command:
```
python run.py --check
```

To run the scraper directly, run the following command on the command line:
```
scrapy crawl gtr
```
Note: scrapy must be installed for this to work.
# Data Wrangling Challenge
This is a script that generates a csv file containing data from the European Union Road Safety Facts and Figures table on https://en.wikipedia.org/wiki/Road_safety_in_Europe

Please note the **facts_and_figures_table.csv** data is displayed according to the 'Road Deaths per Million Inhabitants' from highest to lowest.

## How to Run on your machine
- Clone this repo: `git clone https://github.com/virgoaugustine/eu-road-safety-figures.git`

- Install the script dependencies: `pip3 install -r requirements.txt`

- Run the script: `python3 data_wrangle.py`

## Data Package
A datapackage.json for the generated csv data can be found [here](https://github.com/virgoaugustine/eu-road-safety-figures/blob/main/datapackage/datapackage.json).

## Data Chart
Chart of Road Deaths Per Million Inhabitants by Country can be found [here](https://github.com/virgoaugustine/eu-road-safety-figures/blob/main/Road%20Deaths%20per%20Million%20Inhabitants_chart.jpg).

## Columns Units
- Area: thousands of km<sup>2</sup>
- Population Density: inhabitants per km<sup>2</sup>
- Vehicle Ownership: Per thousand inhabitants.




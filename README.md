# Citi Bike Data Analysis in New York City

This project analyzes daily Citi Bike usage in New York City between 2019 and 2022. It combines bike trip data with historical weather data to explore how seasonality, temperature, precipitation, the COVID-19 lockdown period, and unusual external events affected bike traffic.

## Project Goal

The assignment was to define research questions or hypotheses and answer them using Citi Bike data. The analysis also uses an external weather data source to add context and explain changes in bike usage over time.

The project includes:

- aggregation of monthly Citi Bike trip files into daily ride counts,
- downloading historical weather data for New York City,
- merging bike and weather datasets,
- exploratory data analysis and visualizations,
- analysis of precipitation and temperature effects,
- anomaly detection with the Isolation Forest algorithm.

## Research Questions

The analysis focuses on the following questions:

1. How did daily Citi Bike usage change between 2019 and 2022?
2. Is the COVID-19 lockdown period visible in the ride data?
3. Do rainy or snowy days reduce the number of bike rides?
4. Is higher temperature associated with more bike rides?
5. Which days were unusually different from the general bike traffic pattern?

## Assignment Requirements

The project addresses the main requirements of the assignment:

- It uses Citi Bike data.
- It analyzes more than three months of data.
- It processes and aggregates large raw files into smaller daily datasets.
- It uses an additional external data source: historical weather data.
- It contains visualizations and interpretation of the results.
- It identifies possible external factors affecting bike traffic.

## Data Sources

The project uses two data sources:

- **Citi Bike trip data** - monthly CSV files containing individual bike trips.
- **Open-Meteo Historical Weather API** - daily weather data for New York City, including maximum temperature, minimum temperature, and precipitation.

Raw Citi Bike data is not included in this repository because the files are large. It can be downloaded from:

[https://citibikenyc.com/system-data](https://citibikenyc.com/system-data)

The analysis covers the period from `2019-01-01` to `2022-12-31`.

## Project Structure

```text
.
|-- pdu.ipynb          # main notebook with data processing, analysis, and charts
|-- requirements.txt   # Python dependencies
|-- .gitignore         # ignored local files and folders
`-- README.md          # project documentation
```

After running the notebook, the following files are created:

```text
data/
|-- raw/                         # downloaded Citi Bike CSV files
`-- processed/
    |-- citi_bike_daily.csv      # aggregated daily bike ride counts
    `-- nyc_weather.csv          # daily weather data
```

## How to Run

1. Clone or download this repository.

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Download monthly Citi Bike CSV files for the analyzed period and place them in:

```text
data/raw/
```

The files may also be placed in subfolders because the notebook searches for CSV files recursively.

5. Open the notebook:

```bash
jupyter notebook pdu.ipynb
```

6. Update the raw data path in the notebook if needed. The current notebook contains the author's local path:

```python
raw_data_path = r'F:\citibike-data-analysis\data\raw'
```

If the project is run from the repository root, this can be changed to:

```python
raw_data_path = 'data/raw'
```

7. Run the notebook cells from top to bottom.

## Analysis Workflow

### 1. Citi Bike Data Aggregation

The notebook searches all CSV files in `data/raw/`, reads the trip start date column, and aggregates individual rides into daily ride counts. It supports both Citi Bike column formats used in different years:

- `starttime`,
- `started_at`.

The aggregated dataset is saved as:

```text
data/processed/citi_bike_daily.csv
```

### 2. Weather Data Collection

Historical weather data is downloaded from the Open-Meteo API for New York City coordinates. The following variables are stored:

- daily maximum temperature,
- daily minimum temperature,
- daily precipitation sum.

The weather dataset is saved as:

```text
data/processed/nyc_weather.csv
```

### 3. Data Analysis and Visualization

After merging the bike and weather datasets by date, the notebook creates visualizations showing:

- daily Citi Bike ride counts over time,
- changes around the COVID-19 lockdown period,
- the relationship between precipitation and ride count,
- the relationship between maximum temperature and ride count,
- anomalous days detected by the Isolation Forest model.

## Key Findings

The analysis suggests that Citi Bike traffic in New York City has a clear seasonal pattern. Ride counts tend to increase during warmer months and decrease during winter. The data also shows unusual drops connected with external events, including the beginning of the COVID-19 lockdown period and major snowstorms.

Weather appears to be an important factor in bike usage. Days with precipitation usually have fewer rides, while higher maximum temperatures are generally associated with higher ride counts. The anomaly detection model highlights days that strongly differ from the typical pattern, such as severe snowstorm days or days affected by pandemic restrictions.

## Technologies Used

- Python
- pandas
- matplotlib
- seaborn
- requests
- scikit-learn
- Jupyter Notebook

## Notes

This repository does not include raw Citi Bike data. Before running the full notebook, download the data manually and place it in `data/raw/`.

The notebook contains both data preparation and analysis steps. If `data/processed/citi_bike_daily.csv` and `data/processed/nyc_weather.csv` already exist, the analysis section can be rerun without repeating the raw data aggregation step.

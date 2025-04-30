### Daily Temperature Analyzer
Daily Temperature Analyzer is a Python-based tool for parsing, processing, and analyzing weather observation data — specifically focusing on calculating daily average temperatures at fixed daytime hours (09:00, 12:00, 15:00, and 18:00).

This project is useful for meteorological analysis, climate studies, or personal weather data tracking over long periods.


### Features
Loads Excel weather data exported from meteorological services (e.g., with headers at row 7).

Cleans and preprocesses raw time and temperature fields.

Filters data to include only 09:00, 12:00, 15:00, and 18:00 observations.

Calculates daily average temperatures.

Saves results to Excel and logs the process.

Outputs yearly statistics (mean, min, max daily averages).

Built-in error handling and logging via dailyTemperatureAnalyzer.log.


### How It Works
Load Excel file with weather records (expects timestamp and temperature).

Preprocess: Clean timestamps and convert temperature to float values.

Filter: Keep only specific hours during the day.

Aggregate: Group by date and year, then calculate the mean temperature.

Export the result to an Excel file.

Log key steps and any warnings/errors.


### Example Directory Structure
project/

├── resources/

│   ├── 27612.01.05.2010.01.05.2025.1.0.0.ru.utf8.00000000.xls

│   └── result.xlsx

│

├── dailyTemperatureAnalyzer.py

├── dailyTemperatureAnalyzers.log

└── README.md

### Dependencies
Python 3.12

pandas

openpyxl (for Excel export)

Install dependencies via:

pip install pandas openpyxl


### Usage
Set input and output paths in main():

python

source_path = r'C:\path\to\your\weather_file.xls'
export_path = r'C:\path\to\save\weather_results.xlsx'
analyzer = WeatherAnalyzer(source_path, export_path)
analyzer.run()
Make sure the Excel file has the expected columns:

"Местное время в Москве (ВДНХ)"

"T" (temperature in Celsius)


### Logging
All key actions and errors are logged in dailyTemperatureAnalyzer.log. This includes:

File loading

Data processing steps

Filtered row counts

Export confirmation

Warnings for missing or malformed data

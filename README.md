# Data Log Visualization

# CLI
> python csv_processor.py 'System_Sensor_log0.csv' 'test.csv'
- Cleans the csv file at the path by replacing commas with decimal points and saves the clean data to the second argument

> python csv_processor.py 'System_Sensor_log0.csv'
- Cleans the csv file at the provided path and overwrites the csv file with the clean data

> python generate_plot.py 'Logs/System_Sensor_log0.csv' 'Logs/testing.csv'
- Cleans data in csv file and saves to second argument. Also, generates an html file with an interactive graph

> python generate_plot.py 'Logs/System_Sensor_log0.csv' 
- Cleans data in csv file and overwrites csv with the clean data. Also, generates an html file with an interactive graph
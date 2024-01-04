import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load JSON data
with open('sample_employee_data.json', 'r') as file:
    sampleData = json.load(file)

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Convert JSON to DataFrame
df = pd.json_normalize(sampleData)


def plot_pie_chart(series, column_name):
    series.value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title(f'Distribution of {column_name}')
    plt.ylabel('')
    plt.show()


def plot_bar_graph(series, column_name):
    series.value_counts().plot(kind='bar')
    plt.title(f'Bar Graph for {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.show()


def plot_line_graph(series, column_name):
    df[column_name] = pd.to_datetime(series)
    df['Year'] = df[column_name].dt.year
    year_values = df['Year'].value_counts().sort_index()
    year_values.plot(kind='line', marker='o')
    plt.title(f'Employee Joining Over Years - {column_name}')
    plt.xlabel('Year')
    plt.ylabel('Number of Employees')
    plt.grid(True)
    plt.show()


def analyze_chart_type(series, column_name):
    unique_values = len(series.unique())

    if 2 <= unique_values <= 5:
        plot_pie_chart(series, column_name)
    elif unique_values >= 40:
        value_check = identify_type(series.iloc[0])
        if value_check == 'datetime':
            plot_line_graph(series, column_name)
    elif 6 <= unique_values <= 39:
        plot_bar_graph(series, column_name)


def identify_type(value: str):
    try:
        int(value)
        return type(int(value)).__name__
    except ValueError:
        pass

    try:
        float(value)
        return type(float(value)).__name__
    except ValueError:
        pass

    if value.lower() in ["true", "false"]:
        # print("boolean")
        return "boolean"

    try:
        format_string = "%Y-%m-%dT%H:%M:%S.%fZ"
        date = datetime.strptime(value, format_string)
        print(type(type(date).__name__))
        return type(date).__name__

    except ValueError:
        pass

    return "string"


def main():
    for column in df.columns:
        try:
            analyze_chart_type(df[column], column)
        except Exception as e:
            print(f"Error processing column '{column}': {e}")


if __name__ == '__main__':
    main()

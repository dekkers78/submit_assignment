import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # I am using Linux

def plot_financial_summary(file='financial_summary_year.csv'):
    try: # Read the CSV file
        data = pd.read_csv(file)
    except FileNotFoundError:
        print(f"The file {file} was not found.")
        return
    required_columns = ['Start Date', 'End Date', 'Total Revenue', 'Total Costs', 'Total Profit'] # Check if the expected columns exist
    for col in required_columns:
        if col not in data.columns:
            print(f"Missing column in the file: {col}")
            return
    summary = data.iloc[0] # Assuming there is only one row in the CSV for this financial summary.

    # If `start_date` and `end_date` are in string format, you might want to convert them to datetime
    start_date = pd.to_datetime(summary['Start Date'])
    end_date = pd.to_datetime(summary['End Date'])
    total_revenue = summary['Total Revenue']
    total_costs = summary['Total Costs']
    total_profit = summary['Total Profit']
    # Create the plot
    labels = ['Total Revenue', 'Total Costs', 'Total Profit']
    values = [total_revenue, total_costs, total_profit]
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, values, color=['green', 'red', 'blue'])
    ax.set_title(f'Financial Summary from {start_date.date()} to {end_date.date()}')
    ax.set_ylabel('Amount')
    ax.set_xlabel('Categories')
    # Add data labels on top of the bars
    for i, value in enumerate(values):
        ax.text(i, value, f'{value:.2f}', ha='center', va='bottom')
    # Display the plot
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()
    
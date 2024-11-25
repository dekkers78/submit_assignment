import csv
from datetime import datetime, timedelta

flag_today = False # Global variables
flag_yesterday = False

def read_initial_date(filename='inner_date.txt'):
    try:
        with open(filename, 'r') as file: # Read the initial date from a file.
            initial_date_str = file.read().strip()
            return datetime.strptime(initial_date_str, '%Y-%m-%d').date()  # Returns date with hours and seconds
    except FileNotFoundError:
        raise FileNotFoundError("Error: inner_date.txt file not found.")
    except ValueError:
        raise ValueError("Error: Incorrect date format in inner_date.txt.")

def parse_date(date_str): # Convert a date string into a datetime object.
    if not date_str:
        raise ValueError("Received an invalid date string: None or empty")
    return datetime.strptime(date_str, '%Y-%m-%d').date()  # Ensures it return a date, cnow onvert it in the given format

def calculate_bought_revenue(filename, start_date, end_date): # Calculate total revenue from bought items within the specified date range.
    total_revenue = 0 # Assign a value
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try: # retrieves the date from the current row of the CSV file and converts it into a datetime object for easier comparison
                row_date = parse_date(row.get('Date')) # Uses the get method of the row dict. to retrieve the value with the key 'Date'.
                # Call the function parse_date to convert the string in a datetime object
                quantity = float(row.get('Quantity', 0) or 0) # Get the correct number and convert it to a float
                buy_price = float(row.get('Buy Price', 0) or 0)
                if start_date <= row_date <= end_date:
                    total_revenue += quantity * buy_price # If start_date is previous or equal to row_date and row_date previous or equal to end_date
            except ValueError as e:
                print(f"Error processing row {row}: {e}")
    return total_revenue

def calculate_sold_revenue(filename, start_date, end_date): # Calculate total revenue from sold items within the specified date range.
    total_revenue = 0
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try: # The same comments as calculate_bought_revenue
                row_date = parse_date(row.get('Date'))
                quantity_sold = float(row.get('Quantity Sold', 0) or 0)
                price_sold = float(row.get('Price Sold', 0) or 0)
                if start_date <= row_date <= end_date:
                    total_revenue += quantity_sold * price_sold
            except ValueError as e:
                print(f"Error processing row {row}: {e}")
    return total_revenue

def get_date_ranges(input_date=None): # Calculate date ranges for current week, month, year or specified date.
    today = read_initial_date()
    global flag_yesterday, flag_today
    if input_date == "yesterday":
        flag_yesterday = True
        input_date = today - timedelta(days=1)
        return input_date, input_date  # Return date objects
    elif input_date == "today":
        flag_today = True
        input_date = today
        return input_date, input_date # Return date objects
    elif input_date is None:
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        month_start = today.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        year_start = today.replace(month=1, day=1)
        year_end = today.replace(month=12, day=31)
        
        return {
            "current_week": (week_start, week_end),
            "current_month": (month_start, month_end),
            "current_year": (year_start, year_end)
        }
    else:
        parts = input_date.split('-') # The result of the split operation is a list containing the substrings that were separated by the delimiter.
        if len(parts) == 1:
            year = int(parts[0]) # Part 0 gives you the year, convert the string into an integer
            start_date = datetime(year, 1, 1).date()  # Ensure it's a date object, 1st day of the year
            end_date = datetime(year, 12, 31).date()  # Ensure it's a date object, last day of the year
        elif len(parts) == 2:
            year, month = map(int, parts) # the map function converts these string elements into integers: e.g. year = 2023 and month = 10
            start_date = datetime(year, month, 1).date() # Create a datetime object on a specified date
# This part constructs a datetime obj. for the 1st day of the next month. E.g., if month is 10, this would create a datetime object for Nov. 1, 2023.
# then: substract 1 day, so you get the last day of the current month. December works quite similar. 
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).date() if month < 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
        elif len(parts) == 3:
            date = datetime.strptime(input_date, '%Y-%m-%d').date()
            start_date = date - timedelta(days=date.weekday()) # returns the day of the week as an int.
# For example, if date is Wednesday (day 2), timedelta(days=2) is subtracted, returning the previous Monday.
            end_date = start_date + timedelta(days=6) # Since start_date is Monday, adding 6 days gives us the Sunday of the week
        else:
            raise ValueError("Input format is invalid. Expected formats: 'YYYY', 'YYYY-MM', or 'YYYY-MM-DD'.")
    
    return start_date, end_date

def record_revenue(start_date, end_date, revenue):
    revenue_data = [
        {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "revenue": revenue
        }
    ]
    with open('revenue.csv', mode='a', newline='') as revenue_file:
        fieldnames = ['start_date', 'end_date', 'revenue']
        revenue_writer = csv.DictWriter(revenue_file, fieldnames=fieldnames)
        if revenue_file.tell() == 0:  # Check if file is empty
            revenue_writer.writeheader()
        revenue_writer.writerows(revenue_data)

def record_profit(start_date, end_date, total_profit):
    profit_data = [
        {
            "start_date": start_date.strftime('%Y-%m-%d'), 
            "end_date": end_date.strftime('%Y-%m-%d'),
            "profit": total_profit
        }
    ]
    with open('profit.csv', mode='a', newline='') as profit_file:
        fieldnames = ['start_date', 'end_date', 'profit']
        profit_writer = csv.DictWriter(profit_file, fieldnames=fieldnames)
        if profit_file.tell() == 0:
            profit_writer.writeheader()
        profit_writer.writerows(profit_data)

def revenue_call(args=None):
    global flag_yesterday, flag_today  # Use global variables
    input_date = args
    try:
        date_ranges = get_date_ranges(input_date)  # Ensure this returns a single date for "yesterday"

        # Check if input_date was specifically "yesterday"
        if input_date.lower() == "yesterday":
            flag_yesterday = True
            flag_today = False  
        elif input_date.lower() == "today":
            flag_today = True
            flag_yesterday = False 
        else:
            flag_yesterday = False
            flag_today = False
        start_date, end_date = date_ranges  # Handle tuple case

        # Calculate revenue
        revenue_sold = calculate_sold_revenue('sold.csv', start_date, end_date)
        total_revenue = revenue_sold
        total_revenue = round(total_revenue, 2) # Use the round function and do it up to two digits after the comma

        # Print the total revenue message
        if start_date == end_date: # If input is one day
                if flag_yesterday: # If the flag yesterday is True
                    print(f"Yesterday's revenue: {total_revenue:.2f}")
                elif flag_today:
                    print(f"Today's revenue so far: {total_revenue:.2f}")
        else: # Not today and not yesterday, so multiple days:
                print(f"Total revenue from {start_date} to {end_date}: {total_revenue:.2f}")
                
        # Record the revenue for this date range  
        answer = input('Do you want to store the revenue over the specified time period: y/n ')
        if answer == "y" or answer == "Y": # Users might type a capital y
         record_revenue(start_date, end_date, total_revenue) # Call the function to store the record
        else: 
         pass   # do nothing
    except Exception as e:
        print(f"An error occurred: {e}")

def profit_call(args=None):
    global flag_yesterday, flag_today  # Use global variables
    input_date = args # Use the parsed argument
    try:
        date_ranges = get_date_ranges(input_date) # Same comments for this block
        if input_date.lower() == "yesterday":
            flag_yesterday = True
            flag_today = False  
        elif input_date.lower() == "today":
            flag_today = True
            flag_yesterday = False 
        else:
            flag_yesterday = False
            flag_today = False
        start_date, end_date = date_ranges 

        # Calculate profit
        revenue_bought = calculate_bought_revenue('bought.csv', start_date, end_date)
        revenue_sold = calculate_sold_revenue('sold.csv', start_date, end_date)
        total_profit = revenue_sold - revenue_bought # The income minus the costs, should be a positive number
        total_profit = round(total_profit, 2) # Round it correct again

        # Print the total revenue message
        if start_date == end_date:
                if flag_yesterday:
                    print(f"Yesterday's profit: {total_profit:.2f}")
                elif flag_today:
                    print(f"Today's profit so far: {total_profit:.2f}")
        else:
                print(f"Total profit from {start_date} to {end_date}: {total_profit:.2f}")

        # Record the revenue for this date range  
        answer = input('Do you want to store the total profit over the specified time period: y/n ')
        if answer == "y" or answer == "Y":
         record_profit(start_date, end_date, total_profit)
        else: 
         pass
    except Exception as e:
        print(f"An error occurred: {e}")
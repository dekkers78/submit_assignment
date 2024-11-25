from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from time_module import restore_inner_date, initial_date_object # Access the date object from another module
import csv, os

inventory = [] # Global variable to store inventory
restore_inner_date() # Call the function to restore the inner date
from time_module import initial_date_object
day = initial_date_object.strftime('%Y-%m-%d') # Convert the date to a string format and store it

def lookup_date_inventory(args):
    console = Console()  # Initialize the console and table using Rich
    table = Table(title="Inventory")
    # Adding columns to the table
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Quantity", justify="center", style="magenta")
    table.add_column("Price", justify="center", style="green")
    table.add_column("Expiration Date", justify="center", style="yellow")
    table.add_column("Date", justify="center", style="blue")

    dates = []
    rows = []

    try:  # Read the initial date
        with open('inner_date.txt', 'r') as file:
            initial_date_str = file.read().strip()
            initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
            input_date = initial_date_object.date()
    except FileNotFoundError:
        console.print("Error: inner_date.txt file not found.", style="bold red")
        return
    except ValueError:
        console.print("Error: Incorrect date format in inner_date.txt.", style="bold red")
        return

    if args == "now":
        input_date  # Take the current date
    elif args == "yesterday":
        input_date = input_date - timedelta(days=1)  # Current date minus 1
    else:  # If the argument is not "now" or "yesterday", parse it as a date
        try:
            input_date = datetime.strptime(args, '%Y-%m-%d').date()
        except ValueError:
            console.print("Error: Invalid date format provided. Use 'YYYY-MM-DD'.", style="bold red")
            return
    try:  # Open the CSV file and read the data
        with open('inventory.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for column in reader:
                if len(column) > 4:
                    date_str = column[4].strip()  # Extract date from column 5
                    rows.append(column)  # Store the entire row for later use
                    dates.append(date_str)  # Collect dates
    except FileNotFoundError:
        console.print("Error: inventory.csv file not found.", style="bold red")
        return
    found = False
    for column in rows:  # Iterate over the stored rows to find matches
        if len(column) > 4:
            date_str = column[4].strip()
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                console.print(f"Warning: Incorrect date format in CSV at column: {column}", style="bold yellow")
                continue
            if (input_date - date).days == 0:
                # If a match is found, print the row in the table
                table.add_row(column[0], column[1], column[2], column[3], date_str)
                found = True
    if found:  # is True
        console.print(table)  # Display the prepared table
    else:
        console.print(f"No matching dates found for {input_date}.", style="bold red")

def load_inventory(file_path): # Load inventory from a CSV file. 
    global inventory
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header row
            inventory = []  # Reset inventory
            for column in reader:
                inventory.append([column[0], int(column[1]), float(column[2]), column[3], column[4]])
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating brand new inventory!") # User friendly message
    return inventory

def buy_product(args): # Handle the purchase of a product.
    if args.price < 0: # Reject negative prices
        print("ERROR: Price cannot be negative.")
        return 
    global inventory, day  # Inventory and day are global variables
    load_inventory('inventory.csv') # Call function 'load_inventory'
    found = False  # Flag to track if an item was found
    for item in inventory: # Loop through inventory to find items that match the given product
        if (item[0] == args.product_name and # Compare product names, expiration dates, and price with tolerance
            item[3] == args.expiration_date and 
            abs(item[2] - float(args.price)) < 0.01 and # convert args.price to a float and check if they compare up to less than 1 cent difference
            item[4] == day): # allowing for minor rounding errors :( that can occur in floating-point arithmetic.
            # If item is found, update only its quantity
            item[1] += args.quantity  # Increase ONLY the quantity in the inventory list
            found = True  # Item found
            break  # Exit loop since we found the product
    if not found: # If no existing item was found, create a new entry
        new_item = [
            args.product_name,
            args.quantity,
            float(args.price),
            args.expiration_date,
            day
        ]
        inventory.append(new_item)  # Append (add a new line) new item to inventory list
    # Save the updated inventory back to the CSV (so updated quantities or new entries)
    with open('inventory.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Quantity', 'Price', 'Expiration Date', 'Date'])  # Write header row
        for item in inventory:  # Write all items back to the file
            writer.writerow([item[0], item[1], item[2], item[3], item[4]])

    file_exists = os.path.isfile('bought.csv') # Check if the file exists
    with open('bought.csv', mode='a', newline='') as bought_file: # Also log the purchase to 'bought.csv'
        bought_writer = csv.writer(bought_file) # Initialize writer object      
        if not file_exists: # Write the header if the file did not exist before
         bought_writer.writerow(['Product Name', 'Quantity', 'Buy Price', 'Expiration Date', 'Date'])    
        bought_row = [
            args.product_name,
            args.quantity,
            float(args.price),
            args.expiration_date,
            day
        ]
        bought_writer.writerow(bought_row)  # Append / write the purchase record
        print("OK") # Display the OK message in console

def display_inventory():
    table = Table(title="Inventory", title_justify="center")
    # Define the columns
    table.add_column("Product Name", justify="left", style="yellow")
    table.add_column("Quantity", justify="right", style="magenta")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Expiration Date", justify="right", style="cyan")
    table.add_column("Date", justify="right", style="green")
    load_inventory('inventory.csv')  # Ensure inventory is loaded before displaying
    if not inventory:  # Check if inventory is loaded
        console.print("Inventory is empty.", style="bold red")
        return

    for item in inventory:
        table.add_row(
            item[0], 
            str(item[1]), 
            f"€{item[2]:.2f}", 
            item[3],
            item[4]
        )

    console = Console()  # Create a console object
    console.print(table)  # Print the table to the console

def sell_product(args): # Handle the sale of a product.
    if args.price < 0: 
        print("ERROR: Price cannot be negative.")
        return
    load_inventory('inventory.csv') 
    found = False  
    for item in inventory:
        # Compare product names and prices
        if item[0] == args.product_name:
            if item[1] >= args.quantity:  # Ensure sufficient quantity for sale
                found = True  # Set found to True
                item[1] -= args.quantity  # Decrease the quantity by argument given for sale
                current_date = day  # Getting current date
                price_to_use = str(args.price) # Convert price (float) to a string and store it in price_to_use
                file_exists = os.path.isfile('sold.csv')
                with open('sold.csv', mode='a', newline='') as sold_file: # Log sold item details to sold.csv in append modus
                    writer = csv.writer(sold_file)
                    # Write header if the file does not exist
                    if not file_exists:
                        writer.writerow(['Product Name', 'Quantity Sold', 'Price Sold', 'Expiration Date', 'Date'])
                    writer.writerow([item[0], args.quantity, price_to_use, item[3], current_date]) # Write item details to sold.csv
                    print("OK")
                # Check if quantity is now zero and remove item from inventory if it is
                if item[1] <= 0:
                    inventory.remove(item)
            else:
                print(f"Cannot sell {args.quantity} of {item[0]}. Not enough quantity available.")
            break  # Exit loop since we found the product
    if not found:
        print("ERROR: Product not in stock.")

    with open('inventory.csv', mode='w', newline='') as file: # Save the updated inventory back to the CSV
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Quantity', 'Price', 'Expiration Date', 'Date'])  # Write header
        for item in inventory:  # Write all items back to the file
            writer.writerow([item[0], item[1], item[2], item[3], item[4]])
    
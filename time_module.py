from datetime import datetime, timedelta

initial_date_object = None # It needs to have some value -> none (global variable)

def first_start_set_date(): 
 date_format = '%Y-%m-%d'  # Desired datetime format
 while True:  # Loop until valid input is given
  initial_date_str = input("Enter initial date and time (YYYY-MM-DD): ")  
  try: # Try to parse the input string into a datetime object
   initial_date_object = datetime.strptime(initial_date_str, date_format) # Take the string and format it in a datetime object using date_format
   break  # Exit the loop if input is valid
  except ValueError: # Handle the case where the input format is incorrect
   print(f"Invalid input format. Please use the format: YYYY-MM-DD")    
 with open('inner_date.txt', 'w') as file: # Writes a file, even if it did not exist beforehand (very nice)
  file.write(initial_date_str) # Write the string value
  print("Thanks for setting current date and time.") # A user friendly message

def set_date(args):
    set_date_str = args.set  # Store the parsed argument in a variable
    while True:  # Loop until valid input is given
        try:  # Try to parse the input string into a datetime object
            initial_date_object = datetime.strptime(set_date_str, '%Y-%m-%d')
            break  # Exit the loop if input is valid
        except ValueError:  # Handle the case where the input format is incorrect
            print(f"Invalid input format: '{set_date_str}'. Please use the format: YYYY-MM-DD")
            return  # Exit the function if the format is incorrect
    # If input is valid, write it to the file
    with open('inner_date.txt', 'w') as file:
        file.write(set_date_str)
        print("Thanks for setting current date and time.")

def restore_inner_date():
 global initial_date_object  # Make known the variable as global
 try:
  with open('inner_date.txt', 'r') as file:
   initial_date_str = file.read().strip() # Take away whitespaces
   initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
 except FileNotFoundError:
        print("Error: inner_date.txt file not found.")
        first_start_set_date() # Call the function were you start setting the date for the first time
        restore_inner_date() # With the file prepared, loop through the function again, it won't bump against FileNotFoundError
 except ValueError:
        print("Error: Incorrect date format in inner_date.txt. Expected format: YYYY-MM-DD.")
 except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

def restore_inner_date_print():
  print(initial_date_object.date()) # Display the date without hours, minutes, seconds  

def advance_time_function(nr_days_by_user): # Give one argument
 with open('inner_date.txt', 'r') as file:
  initial_date_str = file.read().strip()
  initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
  new_date = initial_date_object + timedelta(days=nr_days_by_user) # Store a new_date with a number of input given days
  date_string = new_date.strftime("%Y-%m-%d") # Convert a datetime object back to a string for storage
 with open('inner_date.txt', 'w') as file:
  file.write(date_string) # Write the date string
  print("OK") # Display OK in console
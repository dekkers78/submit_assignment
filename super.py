import argparse, os
from inventory_module import buy_product, sell_product, lookup_date_inventory
from time_module import first_start_set_date, restore_inner_date, set_date, restore_inner_date_print, advance_time_function
from economic_module import revenue_call, profit_call
from plot_graphics_module import plot_financial_summary

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

def lowercase_string(value): # Convert input value to lowercase.
    return value.lower()

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="SuperPy - a supermarket management system", epilog="SuperPy, the manager that works for you! - 2024")
    parser.add_argument('--advance-time', type=int, required=False, help="Specify the advancement of a time period (in days)")
    parser.add_argument('--yesod', required=False, action='store_true')
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command")
    # Create the 'buy' subparser
    buy_parser = subparsers.add_parser("buy", help="To purchase a product, e.g. 'Milk' '€1.00' type: buy --product-name milk --price 1")
    # Add arguments to the 'buy' subparser
    buy_parser.add_argument("--product-name", type=lowercase_string, required=True, help="Name of the product to buy (e.g., milk, bread)")
    buy_parser.add_argument("--quantity", type=int, default=1, help="Quantity to buy (default is 1 item)")
    buy_parser.add_argument("--price", type=float, required=True, help="Price of the product")
    buy_parser.add_argument("--expiration-date", type=lowercase_string, default="None", help="Expiration date of the product (YYYY-MM-DD)")
    # Create the 'plot' subparser
    plot_parser = subparsers.add_parser("plot", help="Display the 'financial year summery' csv file in graphics")
    # Create the 'sell' subparser
    sell_parser = subparsers.add_parser("sell", help="To sell a product, e.g. 'Teddybear' '€19.95' type: sell --product-name teddybear --price 19.95")
    # Add arguments to the 'sell' subparser
    sell_parser.add_argument("--product-name", type=lowercase_string, required=True, help="Name of the product to sell")
    sell_parser.add_argument("--quantity", type=int, default=1, help="Quantity to sell (default is 1)")
    sell_parser.add_argument("--price", type=float, required=True, help="Price of the product")
    sell_parser.add_argument("--expiration-date", type=lowercase_string, default="None", help="Expiration date of the product (YYYY-MM-DD)")

    report_parser = subparsers.add_parser('report', help='Make reports: inventory/revenue/profit,    e.g. type: report inventory --date 2019-11-11')
    report_subparsers = report_parser.add_subparsers(dest='subcommand', help='Subcommands for reports')

    # Subparser for inventory report
    inventory_parser = report_subparsers.add_parser('inventory', help='Report inventory')
    inventory_parser.add_argument('--date', type=lowercase_string, help='Specify the date for the inventory report', required=False)
    inventory_parser.add_argument('--yesterday', action='store_true', help='Get inventory report for yesterday')
    inventory_parser.add_argument("--now", action='store_true', help='Get inventory report for today')

    # Subparser for revenue report
    revenue_parser = report_subparsers.add_parser('revenue', help='Report revenue')
    revenue_parser.add_argument('--date', type=lowercase_string, help='Specify the date for the revenue report', required=False)
    revenue_parser.add_argument('--yesterday', action='store_true', help='Get inventory report for yesterday')
    revenue_parser.add_argument("--today", action='store_true', help='Get inventory report for today')

    # Subparser for profit report
    profit_parser = report_subparsers.add_parser('profit', help='Report profit')
    profit_parser.add_argument('--date', type=lowercase_string, help='Specify the date for the profit report', required=False)
    profit_parser.add_argument('--yesterday', action='store_true', help='Get inventory report for yesterday')
    profit_parser.add_argument("--today", action='store_true', help='Get inventory report for today')
    # Create the 'time' subparser
    time_parser = subparsers.add_parser("time", help="Display current date and time. To set to a different date, type: time --set, ")
    # Add argument to the 'time' subparser
    time_parser.add_argument("--set", type=lowercase_string, help="Use the YYYY-MM-DD format")

    # Parse the command line arguments
    args = parser.parse_args()
    
    if not os.path.exists('inner_date.txt'): # If the file does not exists then call first_start_set_date function
     first_start_set_date()
    else:  # If the file exists, read the stored date to get the variable in the memory
     restore_inner_date()

# Check the command arguments
    if args.command == 'plot':
     plot_financial_summary()
    elif args.advance_time is not None: # You should give one argument
        advance_time_function(args.advance_time)
    elif args.yesod: # The most important command
      print('John 3:16 ❤️ ❤️ ❤️ \n For God so loved the world that He gave His only begotten Son, \n that whoever believes in Him should not perish but have everlasting life.')    
    elif args.command == "time":
     if args.set: 
        set_date(args)  # Call function set_date
     else:
        restore_inner_date_print()
    elif args.command == "buy":
     buy_product(args)
    elif args.command == "sell":
     sell_product(args)
    elif args.command == 'report' :
     if args.subcommand == 'inventory':
      if args.yesterday:
       lookup_date_inventory(args="yesterday") # We know args should be yesterday and this simply works :)
      elif args.date:
       lookup_date_inventory(args.date)   
      elif args.now:
       lookup_date_inventory(args="now") 
      else:
        print("You must specify either --date or --now or --yesterday.") # Give feedback were the input is incorrect
      
     elif args.subcommand == 'revenue':
      if args.yesterday:
        revenue_call(args="yesterday")
      elif args.date:
        revenue_call(args.date)
      elif args.today:
        revenue_call(args="today")
      else: 
        print("You must specifiy either --date or --now or --yesterday.")
     elif args.subcommand == 'profit':
       if args.yesterday:
         profit_call(args="yesterday")
       elif args.date:
         profit_call(args.date)
       elif args.today:
         profit_call(args="today")
       else: 
         print("You must specify either --date or --now or --yesterday.") 
        
if __name__ == "__main__":
    main()    
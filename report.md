# Super Py - The Supermarket System that works for you!

**Programmer:** Eric Dekkers  
**Date:** November 25, 2024  

## a 300-Word Report

This report provides snippets of techniques that I have used to write this program.

## Key Highlights

- A function called *restore_inner_date*
- A snippet from *buy_product*
- A function called *lowercase_string*

## Restore Inner Date

```python def restore_inner_date():
 global initial_date_object
 try:
  with open('inner_date.txt', 'r') as file:
   initial_date_str = file.read().strip() 
   initial_date_object = datetime.strptime(initial_date_str, '%Y-%m-%d')
 except FileNotFoundError:
        print("Error: inner_date.txt file not found.") # Prints a user friendly message
        first_start_set_date() # <- call this function
        restore_inner_date() # <- with the date (file) prepared, simply loop through this function again, it won't give FileNotFoundError
        # so now you end up having a file called inner_date.txt and are ready to continue
```
## Snippet from buy_product
```python
if (item[0] == args.product_name and 
            item[3] == args.expiration_date and 
            abs(item[2] - float(args.price)) < 0.01 and 
            item[4] == day): 
            # If all criteria match, don't add another line, simply update the inventory to the right quantity, so there are no unnecessary, ugly lines.
            item[1] += args.quantity # <- <- <-
```
## Snippets that belong to **lowercase_string** 
```python
def lowercase_string(value): # This small function ensures that all input strings are converted to lowercase values.
    return value.lower() # This is a compact and consistent way of doing that.

**plus**

buy_parser.add_argument("--product-name", type=lowercase_string, required=True, help="Name of the product to buy (e.g., milk, bread)")


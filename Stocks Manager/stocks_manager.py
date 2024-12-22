import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create database and table if they don't exist
def init_db():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            ticker TEXT PRIMARY KEY,
            quantity INTEGER,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new stock entry
def add_stock():
    ticker = item_name_entry.get().strip().upper()
    quantity = item_qty_entry.get().strip()
    price = item_price_entry.get().strip()

    if not ticker or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
        messagebox.showerror("Input Error", "Please provide valid ticker, quantity, and price.")
        return

    quantity = int(quantity)
    price = float(price)

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    # Check if the stock already exists in the database
    cursor.execute('SELECT quantity, price FROM stocks WHERE ticker = ?', (ticker,))
    existing_stock = cursor.fetchone()

    if existing_stock:
        # If stock exists, calculate the new weighted average price
        existing_quantity, existing_price = existing_stock
        total_quantity = existing_quantity + quantity
        new_price = ((existing_quantity * existing_price) + (quantity * price)) / total_quantity

        # Update the stock with the new quantity and weighted average price
        cursor.execute('UPDATE stocks SET quantity = ?, price = ? WHERE ticker = ?', (total_quantity, new_price, ticker))
        result_label.config(text=f'Updated {ticker} with new total {total_quantity} shares at weighted price {new_price:.2f}')
    else:
        # If stock does not exist, insert it as a new entry
        cursor.execute('INSERT INTO stocks (ticker, quantity, price) VALUES (?, ?, ?)', (ticker, quantity, price))
        result_label.config(text=f'Added {ticker} with {quantity} shares at {price:.2f}')

    conn.commit()
    conn.close()
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    item_price_entry.delete(0, tk.END)

# Function to update an existing stock entry
def update_stock():
    ticker = item_name_entry.get().strip().upper()
    quantity = item_qty_entry.get().strip()
    price = item_price_entry.get().strip()

    if not ticker or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
        messagebox.showerror("Input Error", "Please provide valid ticker, quantity, and price.")
        return

    quantity = int(quantity)
    price = float(price)

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE stocks SET quantity = ?, price = ? WHERE ticker = ?', (quantity, price, ticker))
    conn.commit()

    if cursor.rowcount == 0:
        result_label.config(text=f'{ticker} not found in the database.')
    else:
        result_label.config(text=f'Updated {ticker} to {quantity} shares at {price:.2f}')

    conn.close()
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    item_price_entry.delete(0, tk.END)

# Function to search and display a stock entry
def search_stock():
    ticker = item_name_entry.get().strip().upper()

    if not ticker:
        messagebox.showerror("Input Error", "Please enter a ticker to search.")
        return

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ticker, quantity, price FROM stocks WHERE ticker = ?', (ticker,))
    stock = cursor.fetchone()

    if stock:
        result_label.config(text=f'{stock[0]}: {stock[1]} shares at {stock[2]:.2f}')
    else:
        result_label.config(text=f'{ticker} not found in the database.')

    conn.close()
    item_name_entry.delete(0, tk.END)

# Function to remove an existing stock entry
def remove_stock():
    ticker = item_name_entry.get().strip().upper()

    if not ticker:
        messagebox.showerror("Input Error", "Please enter a ticker to remove.")
        return

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM stocks WHERE ticker = ?', (ticker,))
    conn.commit()

    if cursor.rowcount == 0:
        result_label.config(text=f'{ticker} not found in the database.')
    else:
        result_label.config(text=f'Removed {ticker} from the database.')

    conn.close()
    item_name_entry.delete(0, tk.END)

# Function to generate a full list of stocks
def generate_stock_list():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ticker, quantity, price FROM stocks')
    stocks = cursor.fetchall()

    if not stocks:
        result_label.config(text='No stocks in the database.')
        return

    stock_list = [f'{stock[0]}: {stock[1]} shares at {stock[2]:.2f}' for stock in stocks]
    result_label.config(text='\n'.join(stock_list))

    conn.close()

# Function to remove all stock entries
def remove_all_stocks():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM stocks')
    conn.commit()

    result_label.config(text='All stocks have been removed from the database.')
    conn.close()

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Stock Management")

# Input fields
item_name_label = tk.Label(root, text="Stock Ticker:")
item_name_label.grid(row=0, column=0, padx=5, pady=5)
item_name_entry = tk.Entry(root)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)

item_qty_label = tk.Label(root, text="Quantity:")
item_qty_label.grid(row=1, column=0, padx=5, pady=5)
item_qty_entry = tk.Entry(root)
item_qty_entry.grid(row=1, column=1, padx=5, pady=5)

item_price_label = tk.Label(root, text="Price:")
item_price_label.grid(row=2, column=0, padx=5, pady=5)
item_price_entry = tk.Entry(root)
item_price_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons for stock management
add_button = tk.Button(root, text="Add Stock", command=add_stock)
add_button.grid(row=3, column=0, padx=5, pady=5)

update_button = tk.Button(root, text="Update Stock", command=update_stock)
update_button.grid(row=3, column=1, padx=5, pady=5)

search_button = tk.Button(root, text="Search Stock", command=search_stock)
search_button.grid(row=4, column=0, padx=5, pady=5)

remove_button = tk.Button(root, text="Remove Stock", command=remove_stock)
remove_button.grid(row=4, column=1, padx=5, pady=5)

generate_button = tk.Button(root, text="Generate Stock List", command=generate_stock_list)
generate_button.grid(row=5, column=0, padx=5, pady=5)

# Button to remove all stocks
remove_all_button = tk.Button(root, text="Remove All Stocks", command=remove_all_stocks)
remove_all_button.grid(row=5, column=1, padx=5, pady=5)

# Result display
result_label = tk.Label(root, text="Result will appear here", wraplength=300)
result_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Start the Tkinter main loop
root.mainloop()
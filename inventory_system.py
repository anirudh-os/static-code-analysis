"""A simple JSON-based inventory management system."""

import json
from datetime import datetime


def add_item(inventory, item="default", qty=0, logs=None):
    """Adds an item to the provided inventory dictionary."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        print(f"Error: Invalid type for item or quantity. "
              f"Skipping: ({item}, {qty})")
        return

    if not item:
        return
    inventory[item] = inventory.get(item, 0) + qty
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(inventory, item, qty):
    """Removes a quantity of an item from the inventory."""
    if not isinstance(qty, int):
        print(f"Error: Invalid quantity type. Skipping: ({item}, {qty})")
        return

    try:
        inventory[item] -= qty
        if inventory[item] <= 0:
            del inventory[item]
    except KeyError:
        print(f"Error: Item '{item}' not in inventory. Cannot remove.")


def get_qty(inventory, item):
    """Gets the quantity of a specific item from the inventory."""
    return inventory.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a file and returns it as a dictionary."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. "
              f"Starting with empty inventory.")
        return {}


def save_data(inventory, file="inventory.json"):
    """Saves the provided inventory dictionary to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(inventory, indent=4))


def print_data(inventory):
    """Prints a report of all items in the inventory."""
    print("Items Report")
    for item, qty in inventory.items():
        print(f"{item} -> {qty}")


def check_low_items(inventory, threshold=5):
    """Returns a list of items below a given threshold."""
    return [item for item, qty in inventory.items() if qty < threshold]


def main():
    """Main function to manage the inventory state and call operations."""
    stock_data = load_data()

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", -2)
    add_item(stock_data, 123, "ten")  # invalid types, no check
    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)

    print("Apple stock:", get_qty(stock_data, "apple"))
    print("Low items:", check_low_items(stock_data))

    print_data(stock_data)

    save_data(stock_data)


if __name__ == "__main__":
    main()

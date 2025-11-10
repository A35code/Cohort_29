# 🧾 Simple Inventory Management System (Tkinter + Python)

A desktop-based **Inventory Management System** built with **Python** and **Tkinter**.  
This project allows users to manage products, track stock levels, and perform import/export operations using a clean and interactive GUI.

---

## 🗂️ Project Structure

### Inventory system

`main.py` : Entry point – launches the GUI

`gui.py` : Tkinter interface for the inventory system
`storage.py` : Business logic and data persistence
`models.py` : Product data model
`exceptions.py` : Custom exceptions for validation and error handling


---

## 🧠 Overview

This system provides both **backend logic** and a **frontend GUI** for managing product inventories.  
It supports adding, editing, deleting, and restocking products, while saving data automatically in a JSON file for persistence.

---

## ⚙️ Features

### 🖥️ Graphical User Interface
- Built using **Tkinter** for an easy-to-use experience.
- Displays products in a sortable table with scrollbars.
- Highlights **low-stock items** in red.
- Provides alerts when products fall below reorder level.

### 📦 Product Management
- Add, edit, and delete products with validation.
- Manage suppliers and reorder levels.
- Adjust stock quantities (positive or negative).

### 💾 Data Management
- Data is automatically **saved to JSON** (`inventory_data.json`).
- Supports **CSV import/export** for easy data exchange.

### 🚨 Error Handling
- Handles invalid SKU formats and negative stock operations using **custom exceptions**:
  - `InvalidSKUError`
  - `NegativeStockError`

---

## 🧩 Modules Breakdown

### `main.py`
Launches the entire application.  
Creates the Tkinter window and loads the `InventoryApp` interface from `gui.py`.

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

```

### `gui.py` (InventoryApp)

Implements the Tkinter GUI for user interaction.

Key Functions:

- add_product() → Add new items.

- edit_product() → Modify existing products.

-  delete_product() → Remove a product.

-  adjust_stock() → Update stock quantity.

-  import_csv() / export_csv() → Handle CSV operations.

-  refresh_table() → Updates the product table and alerts.

### `storage.py` (Inventory Class)

Handles data storage, business logic, and file persistence.

Key Responsibilities:

- Validate SKUs (ABC-1234 format).

- Save and load data from inventory_data.json.

- Adjust stock levels safely.

- Detect and return low-stock items.

- Support CSV import/export.

### `models.py` (Product Class)

Defines the Product model, representing each item in the inventory.

Attributes:

- sku

- name

- quantity

- reorder_level

- supplier

- Methods:

- `to_dict()` → Converts product data to a dictionary.

- `from_dict()` → Creates a Product object from saved data.

### `exceptions.py`

Defines custom exception classes to handle specific errors.

Exceptions:

- NegativeStockError → Raised when an operation would cause negative stock.

- InvalidSKUError → Raised when an SKU doesn’t follow the required format.

## 🚀 How to Run
1️⃣ Prerequisites

Ensure you have Python 3.x installed.
Tkinter comes pre-installed with Python.

2️⃣ Run the Application

In your terminal or command prompt, navigate to the project folder and run:

```python
python main.py
```

3️⃣ The GUI Window

Once launched, the application window will appear where you can:

1. Add or edit products

2. Adjust stock

3. Import/export CSV files

4. View low-stock alerts

### 💾 Data Persistence

All product information is saved automatically in:

inventory_data.json


This file is created and updated automatically when you add or modify products.

### 📤 CSV File Format

When importing or exporting products, CSV files follow this structure:

| SKU | Name | Quantity | Reorder Level | Supplier |
|-----|------|-----------|----------------|-----------|
| ABC-1234 | Laptop | 10 | 3 | TechSupplier Ltd |


### 📚 Example Workflow

Click Add Product to enter details like SKU, name, quantity, reorder level, and supplier.

Adjust stock using the Adjust Stock button.

Export data to CSV or import new data from existing files.

Low-stock alerts appear automatically for items below reorder level.

### 🧰 Technologies Used

Python 3

Tkinter (GUI)

JSON (Data storage)

CSV (Import/Export)

OOP Principles (Classes, Encapsulation, Exceptions)

### 🧑‍💻 Author/Creators

Developed by Group 15
1. Hassana Is’haq Musa (Group leader)
2. Akwada Emmanuel Chinedu



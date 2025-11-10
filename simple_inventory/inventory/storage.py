"""Inventory storage and business logic."""
import csv
import re
import json
import os

from models import Product
from exceptions import NegativeStockError, InvalidSKUError


class Inventory:
    def __init__(self):
        self.products = {}
        self.data_file = 'inventory_data.json'
        self.load_data()

    def validate_sku(self, sku):
        """Validate SKU format (e.g., ABC-1234 or ABC-12)"""
        pattern = r'^[A-Z]{3}-\d{2,4}$'
        if not re.match(pattern, sku):
            raise InvalidSKUError("SKU must be in format: ABC-1234 (3 uppercase letters, dash, 2-4 digits)")
        return True

    def add_product(self, product):
        """Add a new product"""
        self.validate_sku(product.sku)
        if product.sku in self.products:
            raise ValueError("Product with this SKU already exists")
        if product.quantity < 0:
            raise NegativeStockError("Initial quantity cannot be negative")
        self.products[product.sku] = product
        self.save_data()

    def update_product(self, sku, name, quantity, reorder_level, supplier):
        """Update existing product"""
        if sku not in self.products:
            raise ValueError("Product not found")
        if quantity < 0:
            raise NegativeStockError("Quantity cannot be negative")

        product = self.products[sku]
        product.name = name
        product.quantity = quantity
        product.reorder_level = reorder_level
        product.supplier = supplier
        self.save_data()

    def delete_product(self, sku):
        """Delete a product"""
        if sku in self.products:
            del self.products[sku]
            self.save_data()

    def adjust_stock(self, sku, adjustment):
        """Adjust stock level (positive or negative)"""
        if sku not in self.products:
            raise ValueError("Product not found")

        product = self.products[sku]
        new_quantity = product.quantity + adjustment

        if new_quantity < 0:
            raise NegativeStockError(f"Cannot reduce stock. Would result in negative quantity: {new_quantity}")

        product.quantity = new_quantity
        self.save_data()

    def get_low_stock_items(self):
        """Get all products below reorder level"""
        return [p for p in self.products.values() if p.quantity <= p.reorder_level]

    def save_data(self):
        """Save inventory to JSON file"""
        data = {sku: product.to_dict() for sku, product in self.products.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        """Load inventory from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.products = {sku: Product.from_dict(pdata)
                                    for sku, pdata in data.items()}
            except Exception:
                self.products = {}

    def export_to_csv(self, filename):
        """Export inventory to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['SKU', 'Name', 'Quantity', 'Reorder Level', 'Supplier'])
            for product in self.products.values():
                writer.writerow([product.sku, product.name, product.quantity,
                            product.reorder_level, product.supplier])

    def import_from_csv(self, filename):
        """Import inventory from CSV"""
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    product = Product(
                        row['SKU'],
                        row['Name'],
                        int(row['Quantity']),
                        int(row['Reorder Level']),
                        row['Supplier']
                    )
                    self.validate_sku(product.sku)
                    self.products[product.sku] = product
                except Exception as e:
                    print(f"Error importing row {row}: {e}")
        self.save_data()

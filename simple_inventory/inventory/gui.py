"""Tkinter GUI for the inventory system."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from storage import Inventory
from models import Product
from exceptions import NegativeStockError, InvalidSKUError


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Inventory System")
        self.root.geometry("900x600")

        self.inventory = Inventory()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Top frame with buttons
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Button(top_frame, text="Add Product", command=self.add_product,
                bg="green", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Edit Product", command=self.edit_product,
                bg="lightblue", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Delete Product", command=self.delete_product,
                bg="red", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Adjust Stock", command=self.adjust_stock,
                bg="orange", fg="white", padx=20).pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Import CSV", command=self.import_csv,
                padx=20).pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="Export CSV", command=self.export_csv,
                padx=20).pack(side=tk.RIGHT, padx=5)

        # Low stock alert frame
        alert_frame = tk.Frame(self.root, bg="#ffebee", pady=5)
        alert_frame.pack(fill=tk.X)

        self.alert_label = tk.Label(alert_frame, text="", bg="#ffebee",
                                fg="#c62828", font=("Arial", 10, "bold"))
        self.alert_label.pack()

        # Table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        self.tree = ttk.Treeview(table_frame,
                                columns=('SKU', 'Name', 'Quantity', 'Reorder Level', 'Supplier'),
                                show='headings',
                                yscrollcommand=scrollbar.set)

        self.tree.heading('SKU', text='SKU')
        self.tree.heading('Name', text='Product Name')
        self.tree.heading('Quantity', text='Stock')
        self.tree.heading('Reorder Level', text='Reorder Level')
        self.tree.heading('Supplier', text='Supplier')

        self.tree.column('SKU', width=100)
        self.tree.column('Name', width=200)
        self.tree.column('Quantity', width=100)
        self.tree.column('Reorder Level', width=120)
        self.tree.column('Supplier', width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Tag for low stock items
        self.tree.tag_configure('low_stock', background='#ffcdd2')

    def refresh_table(self):
        """Refresh the product table"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add products
        for product in self.inventory.products.values():
            tags = ('low_stock',) if product.quantity <= product.reorder_level else ()
            self.tree.insert('', tk.END,
                        values=(product.sku, product.name, product.quantity,
                                product.reorder_level, product.supplier),
                        tags=tags)

        # Update alert
        low_stock = self.inventory.get_low_stock_items()
        if low_stock:
            alert_text = f"⚠ {len(low_stock)} item(s) need reordering: "
            alert_text += ", ".join([f"{p.name} ({p.quantity} left)" for p in low_stock[:3]])
            if len(low_stock) > 3:
                alert_text += f" and {len(low_stock) - 3} more..."
            self.alert_label.config(text=alert_text)
        else:
            self.alert_label.config(text="✓ All items are adequately stocked")

    def add_product(self):
        """Open dialog to add product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        tk.Label(dialog, text="SKU (Format: ABC-1234):").pack(pady=5)
        sku_entry = tk.Entry(dialog, width=30)
        sku_entry.pack()

        tk.Label(dialog, text="Product Name:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()

        tk.Label(dialog, text="Quantity:").pack(pady=5)
        qty_entry = tk.Entry(dialog, width=30)
        qty_entry.pack()

        tk.Label(dialog, text="Reorder Level:").pack(pady=5)
        reorder_entry = tk.Entry(dialog, width=30)
        reorder_entry.pack()

        tk.Label(dialog, text="Supplier:").pack(pady=5)
        supplier_entry = tk.Entry(dialog, width=30)
        supplier_entry.pack()

        def save():
            try:
                product = Product(
                    sku_entry.get().strip().upper(),
                    name_entry.get().strip(),
                    int(qty_entry.get()),
                    int(reorder_entry.get()),
                    supplier_entry.get().strip()
                )
                self.inventory.add_product(product)
                self.refresh_table()
                dialog.destroy()
                messagebox.showinfo("Success", "Product added successfully!")
            except (NegativeStockError, InvalidSKUError, ValueError) as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(dialog, text="Save", command=save, bg="lightgreen",
                fg="white", padx=30, pady=5).pack(pady=5)

    def edit_product(self):
        """Edit selected product"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return

        item = self.tree.item(selected[0])
        sku = item['values'][0]
        product = self.inventory.products[sku]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"SKU: {sku} (cannot be changed)").pack(pady=5)

        tk.Label(dialog, text="Product Name:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, product.name)
        name_entry.pack()

        tk.Label(dialog, text="Stock:").pack(pady=5)
        qty_entry = tk.Entry(dialog, width=30)
        qty_entry.insert(0, str(product.quantity))
        qty_entry.pack()

        tk.Label(dialog, text="Reorder Level:").pack(pady=5)
        reorder_entry = tk.Entry(dialog, width=30)
        reorder_entry.insert(0, str(product.reorder_level))
        reorder_entry.pack()

        tk.Label(dialog, text="Supplier:").pack(pady=5)
        supplier_entry = tk.Entry(dialog, width=30)
        supplier_entry.insert(0, product.supplier)
        supplier_entry.pack()

        def save():
            try:
                self.inventory.update_product(
                    sku,
                    name_entry.get().strip(),
                    int(qty_entry.get()),
                    int(reorder_entry.get()),
                    supplier_entry.get().strip()
                )
                self.refresh_table()
                dialog.destroy()
                messagebox.showinfo("Success", "Product updated successfully!")
            except (NegativeStockError, ValueError) as e:
                messagebox.showerror("Error", str(e))

        tk.Button(dialog, text="Save", command=save, bg="#2196F3",
                fg="white", padx=30, pady=5).pack(pady=20)

    def delete_product(self):
        """Delete selected product"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return

        item = self.tree.item(selected[0])
        sku = item['values'][0]

        if messagebox.askyesno("Confirm", f"Delete product {sku}?"):
            self.inventory.delete_product(sku)
            self.refresh_table()
            messagebox.showinfo("Success", "Product deleted successfully!")

    def adjust_stock(self):
        """Adjust stock for selected product"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product")
            return

        item = self.tree.item(selected[0])
        sku = item['values'][0]
        product = self.inventory.products[sku]

        dialog = tk.Toplevel(self.root)
        dialog.title("Adjust Stock")
        dialog.geometry("350x200")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=f"Product: {product.name}").pack(pady=10)
        tk.Label(dialog, text=f"Current Stock: {product.quantity}").pack(pady=5)

        tk.Label(dialog, text="Adjustment (+ to add, - to remove):").pack(pady=10)
        adj_entry = tk.Entry(dialog, width=20)
        adj_entry.pack()

        def apply():
            try:
                adjustment = int(adj_entry.get())
                self.inventory.adjust_stock(sku, adjustment)
                self.refresh_table()
                dialog.destroy()
                messagebox.showinfo("Success",
                    f"Stock adjusted! New quantity: {self.inventory.products[sku].quantity}")
            except NegativeStockError as e:
                messagebox.showerror("Error", str(e))
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        tk.Button(dialog, text="Apply", command=apply, bg="#FF9800",
                fg="white", padx=30, pady=5).pack(pady=20)

    def export_csv(self):
        """Export inventory to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.inventory.export_to_csv(filename)
            messagebox.showinfo("Success", f"Exported to {filename}")

    def import_csv(self):
        """Import inventory from CSV"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.inventory.import_from_csv(filename)
                self.refresh_table()
                messagebox.showinfo("Success", "CSV imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")

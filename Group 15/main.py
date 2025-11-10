# main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from core2 import InventorySystem, NegativeStockError, InvalidSKUError

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Inventory System")
        self.geometry("800x500")
        self.inv = InventorySystem()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")
        ttk.Button(toolbar, text="Add Product", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Adjust Stock", command=self.adjust_stock).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Export CSV", command=self.export_csv).pack(side="right", padx=5)
        ttk.Button(toolbar, text="Import CSV", command=self.import_csv).pack(side="right", padx=5)

        # Low stock badge
        self.alert_label = ttk.Label(toolbar, text="", foreground="red")
        self.alert_label.pack(side="right", padx=5)

        # Table
        columns = ("Name", "SKU", "Supplier", "Stock", "Reorder Level")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.inv.products.values():
            self.tree.insert("", "end", iid=p.id, values=(p.name, p.sku, p.supplier, p.stock, p.reorder_level))
        low = self.inv.low_stock()
        self.alert_label.config(text=f"Low stock: {len(low)} item(s)" if low else "")

    def add_product(self):
        win = tk.Toplevel(self)
        win.title("Add Product")
        fields = ["Name", "SKU", "Supplier", "Reorder Level", "Initial Stock"]
        entries = {}
        for i, field in enumerate(fields):
            ttk.Label(win, text=field).grid(row=i, column=0, padx=5, pady=5)
            e = ttk.Entry(win)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = e

        def save():
            try:
                name = entries["Name"].get()
                sku = entries["SKU"].get()
                supplier = entries["Supplier"].get()
                reorder = int(entries["Reorder Level"].get() or 0)
                stock = int(entries["Initial Stock"].get() or 0)
                self.inv.add_product(name, sku, supplier, reorder, stock)
                self.refresh_table()
                win.destroy()
            except InvalidSKUError as e:
                messagebox.showerror("Invalid SKU", str(e))
            except ValueError:
                messagebox.showerror("Input Error", "Reorder and stock must be numbers.")
        ttk.Button(win, text="Save", command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def adjust_stock(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a product first.")
            return
        pid = sel[0]
        delta = simpledialog.askinteger("Adjust Stock", "Enter stock adjustment (e.g., -5 or +10):")
        if delta is None: return
        try:
            self.inv.adjust_stock(pid, delta)
            self.refresh_table()
        except NegativeStockError as e:
            messagebox.showerror("Error", str(e))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            self.inv.export_csv(path)
            messagebox.showinfo("Exported", f"Data exported to {path}")

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.inv.import_csv(path)
            self.refresh_table()
            messagebox.showinfo("Imported", f"Data loaded from {path}")

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()

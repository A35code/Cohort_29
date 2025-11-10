import tkinter as tk
from tkinter import messagebox, ttk
from core import InventorySystem, InvalidSKUError, NegativeQuantityError

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System")
        self.root.geometry("850x500")

        self.system = InventorySystem()
        self.system.import_csv()

        # --- UI Layout ---
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Product Name:").grid(row=0, column=0)
        tk.Label(frame_top, text="Price:").grid(row=0, column=2)
        tk.Label(frame_top, text="SKU:").grid(row=0, column=4)
        tk.Label(frame_top, text="Stock:").grid(row=1, column=0)
        tk.Label(frame_top, text="Reorder Level:").grid(row=1, column=2)

        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.sku_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.reorder_var = tk.StringVar()

        tk.Entry(frame_top, textvariable=self.name_var, width=15).grid(row=0, column=1)
        tk.Entry(frame_top, textvariable=self.price_var, width=10).grid(row=0, column=3)
        tk.Entry(frame_top, textvariable=self.sku_var, width=10).grid(row=0, column=5)
        tk.Entry(frame_top, textvariable=self.stock_var, width=10).grid(row=1, column=1)
        tk.Entry(frame_top, textvariable=self.reorder_var, width=10).grid(row=1, column=3)

        tk.Button(frame_top, text="Add Product", command=self.add_product).grid(row=1, column=5, padx=10)

        # --- Table ---
        self.tree = ttk.Treeview(root, columns=("Name", "Price", "SKU", "Stock", "Reorder"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("SKU", text="SKU")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Reorder", text="Reorder Level")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Delete", command=self.delete_product).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Save CSV", command=self.save_csv).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_table).grid(row=0, column=2, padx=5)

        self.refresh_table()

    # ---- Functions ----
    def add_product(self):
        try:
            name = self.name_var.get()
            price = float(self.price_var.get())
            sku = self.sku_var.get()
            stock = int(self.stock_var.get())
            reorder = int(self.reorder_var.get())

            pid = self.system.add_product(name, price, sku, stock, reorder)
            messagebox.showinfo("Success", f"Product '{name}' added!")
            self.refresh_table()

        except InvalidSKUError as e:
            messagebox.showerror("Invalid SKU", str(e))
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values for Price, Stock, and Reorder Level.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return
        pid = self.tree.item(selected[0], "values")[0]
        self.system.delete_product(pid)
        self.refresh_table()

    def save_csv(self):
        self.system.export_csv()
        messagebox.showinfo("Saved", "Inventory saved to CSV.")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.system.products.values():
            self.tree.insert("", tk.END, values=(p.product_id, p.name, p.price, p.sku, p.stock, p.reorder_level))


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

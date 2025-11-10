import csv, re, os, tempfile, uuid
from dataclasses import dataclass, asdict

SKU_RE = re.compile(r'^[A-Z]{3}-\d{4}$')

class NegativeStockError(Exception): pass
class InvalidSKUError(Exception): pass

@dataclass
class Product:
    id: str
    name: str
    sku: str
    supplier: str
    reorder_level: int
    stock: int

class InventorySystem:
    def __init__(self):
        self.products = {}

    def validate_sku(self, sku):
        if not SKU_RE.match(sku):
            raise InvalidSKUError("Invalid SKU format (e.g. ABC-1234).")

    def add_product(self, name, sku, supplier, reorder_level, stock=0):
        self.validate_sku(sku)
        pid = str(uuid.uuid4())
        self.products[pid] = Product(pid, name, sku, supplier, int(reorder_level), int(stock))
        return pid

    def adjust_stock(self, pid, delta):
        prod = self.products[pid]
        new_stock = prod.stock + delta
        if new_stock < 0:
            raise NegativeStockError("Cannot reduce below zero.")
        prod.stock = new_stock

    def low_stock(self):
        return [p for p in self.products.values() if p.stock <= p.reorder_level]

    def export_csv(self, path="data/products.csv"):
        tmp_fd, tmp_path = tempfile.mkstemp()
        with os.fdopen(tmp_fd, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(next(iter(self.products.values()))).keys())
            writer.writeheader()
            for p in self.products.values():
                writer.writerow(asdict(p))
        os.replace(tmp_path, path)

    def import_csv(self, path="data/products.csv"):
        if not os.path.exists(path): return
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.products[row['id']] = Product(**row)
                self.products[row['id']].reorder_level = int(row['reorder_level'])
                self.products[row['id']].stock = int(row['stock'])

"""Product model for the inventory system."""

class Product:
    def __init__(self, sku, name, quantity, reorder_level, supplier):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.supplier = supplier

    def to_dict(self):
        return {
            'sku': self.sku,
            'name': self.name,
            'quantity': self.quantity,
            'reorder_level': self.reorder_level,
            'supplier': self.supplier
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data['sku'],
            data['name'],
            int(data['quantity']),
            int(data['reorder_level']),
            data['supplier']
        )

"""Custom exceptions for the inventory system."""

class NegativeStockError(Exception):
    """Raised when stock level becomes negative"""
    pass


class InvalidSKUError(Exception):
    """Raised when SKU format is invalid"""
    pass

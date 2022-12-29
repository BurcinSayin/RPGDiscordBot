from dataclasses import dataclass


@dataclass
class InventoryItem:
    name: str
    quantity: int

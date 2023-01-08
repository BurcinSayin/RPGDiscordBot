from dataclasses import dataclass


@dataclass
class GlobalItem:
    name: str
    weight: int
    cost: int
    description: str

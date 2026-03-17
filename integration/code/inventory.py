from models import Vehicle
from system import StreetRaceSystem


class InventoryManager:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def add_car(self, car_name: str) -> None:
        name = car_name.strip()
        if not name:
            raise ValueError("Car name cannot be empty.")

        if name in self.system.inventory.cars:
            raise ValueError("Car already exists.")

        self.system.inventory.cars[name] = Vehicle(name=name)

    def get_car(self, car_name: str) -> Vehicle:
        name = car_name.strip()
        if name not in self.system.inventory.cars:
            raise ValueError("Car not found.")
        return self.system.inventory.cars[name]

    def set_car_availability(self, car_name: str, available: bool) -> None:
        car = self.get_car(car_name)
        car.available = available

    def add_spare_part(self, part_name: str, quantity: int = 1) -> None:
        self._validate_item(part_name, quantity)
        name = part_name.strip()

        self.system.inventory.spare_parts[name] = (
            self.system.inventory.spare_parts.get(name, 0) + quantity
        )

    def use_spare_part(self, part_name: str, quantity: int = 1) -> None:
        self._validate_item(part_name, quantity)
        name = part_name.strip()

        current = self.system.inventory.spare_parts.get(name, 0)
        if current < quantity:
            raise ValueError("Not enough spare parts.")

        self.system.inventory.spare_parts[name] = current - quantity

    def add_tool(self, tool_name: str, quantity: int = 1) -> None:
        self._validate_item(tool_name, quantity)
        name = tool_name.strip()

        self.system.inventory.tools[name] = (
            self.system.inventory.tools.get(name, 0) + quantity
        )

    def use_tool(self, tool_name: str, quantity: int = 1) -> None:
        self._validate_item(tool_name, quantity)
        name = tool_name.strip()

        current = self.system.inventory.tools.get(name, 0)
        if current < quantity:
            raise ValueError("Not enough tools.")

        self.system.inventory.tools[name] = current - quantity

    def add_cash(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        self.system.inventory.cash += amount

    def spend_cash(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Amount must be non-negative.")

        if self.system.inventory.cash < amount:
            raise ValueError("Insufficient balance.")

        self.system.inventory.cash -= amount

    def get_cash(self) -> int:
        return self.system.inventory.cash

    def _validate_item(self, name: str, quantity: int) -> None:
        if not name.strip():
            raise ValueError("Item name cannot be empty.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
from roles import Role
from system import StreetRaceSystem


class RepairSystem:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def repair_car(self, car_name: str, part_name: str, tool_name: str, repair_amount: int) -> None:
        name = car_name.strip()
        part = part_name.strip()
        tool = tool_name.strip()

        if repair_amount <= 0:
            raise ValueError("Repair amount must be positive.")

        if name not in self.system.inventory.cars:
            raise ValueError("Car not found.")

        if self.system.inventory.spare_parts.get(part, 0) <= 0:
            raise ValueError("Required spare part unavailable.")

        if self.system.inventory.tools.get(tool, 0) <= 0:
            raise ValueError("Required tool unavailable.")

        mechanic_available = any(m.role == Role.MECHANIC and m.available for m in self.system.crew.values())

        if not mechanic_available:
            raise ValueError("No mechanic available.")

        car = self.system.inventory.cars[name]
        car.condition = min(100, car.condition + repair_amount)

        self.system.inventory.spare_parts[part] -= 1
        self.system.inventory.tools[tool] -= 1

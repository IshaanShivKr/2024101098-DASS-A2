from system import StreetRaceSystem


class VehicleDamage:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def damage_car(self, car_name: str, amount: int) -> None:
        name = car_name.strip()

        if amount < 0:
            raise ValueError("Damage amount cannot be negative.")

        if name not in self.system.inventory.cars:
            raise ValueError("Car not found.")

        car = self.system.inventory.cars[name]
        car.condition = max(0, car.condition - amount)

    def is_car_damaged(self, car_name: str) -> bool:
        name = car_name.strip()

        if name not in self.system.inventory.cars:
            raise ValueError("Car not found.")

        return self.system.inventory.cars[name].condition < 100

from models import Race
from roles import Role
from system import StreetRaceSystem


class RaceManagement:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def create_race(self, race_name: str, driver_name: str, car_name: str) -> None:
        name = race_name.strip()
        driver_name = driver_name.strip()
        car_name = car_name.strip()

        if not name:
            raise ValueError("Race name cannot be empty.")

        if name in self.system.races:
            raise ValueError("Race already exists.")

        if driver_name not in self.system.crew:
            raise ValueError("Driver not registered.")

        driver = self.system.crew[driver_name]

        if driver.role != Role.DRIVER:
            raise ValueError("Only drivers can enter races.")

        if driver.skill is None:
            raise ValueError("Driver skill must be assigned.")

        if not driver.available:
            raise ValueError("Driver not available.")

        if car_name not in self.system.inventory.cars:
            raise ValueError("Car not found.")

        car = self.system.inventory.cars[car_name]

        if not car.available:
            raise ValueError("Car not available.")

        if car.condition <= 0:
            raise ValueError("Car is too damaged to race.")

        race = Race(
            name=name,
            driver=driver,
            car=car,
        )

        self.system.races[name] = race

        driver.available = False
        car.available = False

    def get_race(self, race_name: str) -> Race:
        name = race_name.strip()
        if name not in self.system.races:
            raise ValueError("Race not found.")
        return self.system.races[name]

from system import StreetRaceSystem


class Results:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def record_race_result(self, race_name: str, position: int, prize_money: int) -> None:
        race = self._get_race(race_name)

        if race.completed:
            raise ValueError("Race already completed.")

        if position <= 0:
            raise ValueError("Position must be positive.")

        if prize_money < 0:
            raise ValueError("Prize money cannot be negative.")

        race.position = position
        race.prize_money = prize_money
        race.completed = True

        driver = race.driver
        car = race.car

        self.system.rankings[driver.name] = position

        self.system.inventory.cash += prize_money

        driver.available = True
        car.available = True

    def get_ranking(self, driver_name: str) -> int:
        name = driver_name.strip()
        if name not in self.system.rankings:
            raise ValueError("Ranking not found.")
        return self.system.rankings[name]

    def _get_race(self, race_name: str):
        name = race_name.strip()
        if name not in self.system.races:
            raise ValueError("Race not found.")
        return self.system.races[name]

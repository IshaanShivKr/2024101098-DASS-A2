from models import CrewMember, Inventory, Race, Mission


class StreetRaceSystem:
    def __init__(self):
        self.crew: dict[str, CrewMember] = {}
        self.inventory = Inventory()
        self.races: list[Race] = []
        self.missions: list[Mission] = []
        self.rankings: dict[str, int] = {}

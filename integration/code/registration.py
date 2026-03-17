from roles import Role
from models import CrewMember
from system import StreetRaceSystem


class Registration:
    def __init__(self, system: StreetRaceSystem):
        self.system = system

    def register_member(self, name: str, role: str):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")

        try:
            role_enum = Role(role.strip().lower())
        except ValueError:
            raise ValueError(f"Invalid role: {role}")

        if name in self.system.crew:
            raise ValueError("Member already exists")

        self.system.crew[name] = CrewMember(name=name, role=role_enum)
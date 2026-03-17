from roles import Role
from models import CrewMember
from system import StreetRaceSystem


class Registration:
    def __init__(self, system: StreetRaceSystem):
        self.system = system

    def register_member(self, name: str, role: str) -> None:
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

    def get_member(self, name: str) -> CrewMember:
        clean_name = name.strip()
        if clean_name not in self.system.crew:
            raise ValueError("Crew member not found.")
        return self.system.crew[clean_name]
    
    def list_members(self) -> list[str]:
        return list(self.system.crew.keys())

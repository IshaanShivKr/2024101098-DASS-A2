from roles import Role
from system import StreetRaceSystem


class CrewManagement:
    def __init__(self, system: StreetRaceSystem):
        self.system = system

    def set_skill(self, name: str, skill: int):
        if name not in self.system.crew:
            raise ValueError("Member not found")

        if skill < 0:
            raise ValueError("Skill must be non-negative")

        self.system.crew[name].skill = skill

    def update_role(self, name: str, new_role: str):
        if name not in self.system.crew:
            raise ValueError("Member not found")

        try:
            role_enum = Role(new_role.strip().lower())
        except ValueError:
            raise ValueError(f"Invalid role: {new_role}")

        self.system.crew[name].role = role_enum

    def get_by_role(self, role: Role):
        return [m for m in self.system.crew.values() if m.role == role]
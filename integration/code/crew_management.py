from roles import Role
from system import StreetRaceSystem


class CrewManagement:
    def __init__(self, system: StreetRaceSystem):
        self.system = system

    def update_role(self, name: str, new_role: str) -> None:
        member = self._get_member(name)

        try:
            role_enum = Role(new_role.strip().lower())
        except ValueError as exc:
            raise ValueError(f"Invalid role: {new_role}") from exc

        member.role = role_enum

    def set_skill(self, name: str, skill: int) -> None:
        member = self._get_member(name)

        if skill < 0:
            raise ValueError("Skill must be non-negative.")

        member.skill = skill

    def set_availability(self, name: str, available: bool) -> None:
        member = self._get_member(name)
        member.available = available

    def get_members_by_role(self, role: str) -> list[str]:
        try:
            role_enum = Role(role.strip().lower())
        except ValueError as exc:
            raise ValueError(f"Invalid role: {role}") from exc

        return [
            member.name
            for member in self.system.crew.values()
            if member.role == role_enum
        ]

    def get_available_members_by_role(self, role: Role) -> list[str]:
        return [
            member.name
            for member in self.system.crew.values()
            if member.role == role and member.available
        ]

    def _get_member(self, name: str):
        clean_name = name.strip()
        if clean_name not in self.system.crew:
            raise ValueError("Crew member not found.")
        return self.system.crew[clean_name]

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

from models import Mission
from roles import Role
from mission_types import MissionType
from system import StreetRaceSystem


class MissionPlanning:
    def __init__(self, system: StreetRaceSystem) -> None:
        self.system = system

    def create_mission(
        self,
        mission_name: str,
        mission_type: str,
        required_roles: list[str],
    ) -> None:
        name = mission_name.strip()
        mtype = mission_type.strip().lower()

        if not name:
            raise ValueError("Mission name cannot be empty.")

        if name in self.system.missions:
            raise ValueError("Mission already exists.")

        try:
            mission_type_enum = MissionType(mtype)
        except ValueError as exc:
            raise ValueError(f"Invalid mission type: {mission_type}") from exc

        role_enums = [self._parse_role(r) for r in required_roles]

        self.system.missions[name] = Mission(
            name=name,
            mission_type=mission_type_enum,
            required_roles=role_enums,
        )

    def assign_mission(self, mission_name: str) -> None:
        mission = self._get_mission(mission_name)

        assigned_members = []

        for role in mission.required_roles:
            member = self._find_available_member(role)
            if member is None:
                raise ValueError(f"No available member for role: {role.value}")

            assigned_members.append(member)

        for member in assigned_members:
            member.available = False

        mission.assigned_members = assigned_members

    def start_mission(self, mission_name: str) -> None:
        mission = self._get_mission(mission_name)

        if not mission.assigned_members:
            raise ValueError("Mission must be assigned before starting.")

        if mission.mission_type == MissionType.REPAIR:
            if not any(m.role == Role.MECHANIC for m in mission.assigned_members):
                raise ValueError("Repair mission requires a mechanic.")

        mission.started = True

    def complete_mission(self, mission_name: str) -> None:
        mission = self._get_mission(mission_name)

        if not mission.started:
            raise ValueError("Mission has not started.")

        mission.completed = True

        for member in mission.assigned_members:
            member.available = True

    def _parse_role(self, role: str) -> Role:
        try:
            return Role(role.strip().lower())
        except ValueError as exc:
            raise ValueError(f"Invalid role: {role}") from exc

    def _get_mission(self, mission_name: str) -> Mission:
        name = mission_name.strip()
        if name not in self.system.missions:
            raise ValueError("Mission not found.")
        return self.system.missions[name]

    def _find_available_member(self, role: Role):
        for member in self.system.crew.values():
            if member.role == role and member.available:
                return member
        return None

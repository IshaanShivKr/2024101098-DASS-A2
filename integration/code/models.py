from dataclasses import dataclass, field
from typing import Optional
from roles import Role
from mission_types import MissionType


@dataclass
class CrewMember:
    name: str
    role: Role
    skill: Optional[int] = None
    available: bool = True

@dataclass
class Vehicle:
    name: str
    condition: int = 100
    available: bool = True


@dataclass
class Inventory:
    cars: dict[str, Vehicle] = field(default_factory=dict)
    spare_parts: dict[str, int] = field(default_factory=dict)
    tools: dict[str, int] = field(default_factory=dict)
    cash: int = 0


@dataclass
class Race:
    name: str
    driver: CrewMember
    car: Vehicle
    completed: bool = False
    position: Optional[int] = None
    prize_money: int = 0


@dataclass
class Mission:
    name: str
    mission_type: MissionType
    required_roles: list[Role]
    assigned_members: list[CrewMember] = field(default_factory=list)
    started: bool = False
    completed: bool = False

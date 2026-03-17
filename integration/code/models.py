from dataclasses import dataclass, field
from typing import Optional
from roles import Role

@dataclass
class CrewMember:
    name: str
    role: Role
    skill: Optional[int] = None

@dataclass
class Vehicle:
    name: str
    condition: int = 100

@dataclass
class Inventory:
    cars: dict[str, Vehicle] = field(default_factory=dict)
    cash: int = 0

@dataclass
class Race:
    name: str
    driver: CrewMember
    car: Vehicle
    completed: bool = False
    prize: int = 0

@dataclass
class Mission:
    name: str
    required_roles: list[Role]
    assigned_members: list[CrewMember] = field(default_factory=list)

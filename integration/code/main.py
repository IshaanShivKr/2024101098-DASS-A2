from system import StreetRaceSystem

from registration import Registration
from crew_management import CrewManagement
from inventory import InventoryManager
from race_management import RaceManagement
from results import Results
from mission_planning import MissionPlanning
from damage import VehicleDamage
from repair import RepairSystem


def print_menu() -> None:
    print("\n=== StreetRace Manager ===")
    print("1. Register crew member")
    print("2. Set crew skill")
    print("3. Add car")
    print("4. Create race")
    print("5. Record race result")
    print("6. Create mission")
    print("7. Assign mission")
    print("8. Start mission")
    print("9. Complete mission")
    print("10. Damage car")
    print("11. Repair car")
    print("12. Show status")
    print("0. Exit")


def main() -> None:
    system = StreetRaceSystem()

    reg = Registration(system)
    crew = CrewManagement(system)
    inv = InventoryManager(system)
    race_mgr = RaceManagement(system)
    results = Results(system)
    mission_mgr = MissionPlanning(system)
    damage = VehicleDamage(system)
    repair = RepairSystem(system)

    while True:
        try:
            print_menu()
            choice = input("Select option: ").strip()

            if choice == "0":
                break

            elif choice == "1":
                name = input("Name: ")
                role = input("Role: ")
                reg.register_member(name, role)

            elif choice == "2":
                name = input("Name: ")
                skill = int(input("Skill: "))
                crew.set_skill(name, skill)

            elif choice == "3":
                car = input("Car name: ")
                inv.add_car(car)

            elif choice == "4":
                race = input("Race name: ")
                driver = input("Driver: ")
                car = input("Car: ")
                race_mgr.create_race(race, driver, car)

            elif choice == "5":
                race = input("Race name: ")
                position = int(input("Position: "))
                prize = int(input("Prize money: "))
                results.record_race_result(race, position, prize)

            elif choice == "6":
                name = input("Mission name: ")
                mtype = input("Mission type: ")
                roles = input("Required roles (space separated): ").split()
                mission_mgr.create_mission(name, mtype, roles)

            elif choice == "7":
                name = input("Mission name: ")
                mission_mgr.assign_mission(name)

            elif choice == "8":
                name = input("Mission name: ")
                mission_mgr.start_mission(name)

            elif choice == "9":
                name = input("Mission name: ")
                mission_mgr.complete_mission(name)

            elif choice == "10":
                car = input("Car name: ")
                amt = int(input("Damage amount: "))
                damage.damage_car(car, amt)

            elif choice == "11":
                car = input("Car name: ")
                part = input("Spare part: ")
                tool = input("Tool: ")
                amt = int(input("Repair amount: "))
                repair.repair_car(car, part, tool, amt)

            elif choice == "12":
                print("\n--- STATUS ---")
                print("Crew:", list(system.crew.keys()))
                print("Cars:", list(system.inventory.cars.keys()))
                print("Cash:", system.inventory.cash)
                print("Races:", list(system.races.keys()))
                print("Missions:", list(system.missions.keys()))

            else:
                print("Invalid option.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
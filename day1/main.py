"""
Advent of Code 2019, Day 1
The Tyranny of the Rocket Equation
https://adventofcode.com/2019/day/1
"""

from functools import cache
from os import path

INPUT_FILE = "input.txt"


def read_module_masses(file_path: str) -> list[int]:
    """Read module masses from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@cache
def get_fuel_requirement(mass: int) -> int:
    """Determine the amount of fuel required for a given mass."""

    if mass <= 0:
        return 0

    return mass // 3 - 2


def get_module_fuel_requirement(module_mass: int) -> int:
    """Determine the amount of fuel required strictly for a module."""

    return get_fuel_requirement(module_mass)


@cache
def get_total_fuel_requirement(mass: int) -> int:
    """Determine the amount of fuel required for a module and its fuel."""

    fuel_requirement_for_current_mass = get_fuel_requirement(mass)
    if fuel_requirement_for_current_mass <= 0:
        return 0
    
    fuel_requirement_for_fuel = get_total_fuel_requirement(fuel_requirement_for_current_mass)

    return fuel_requirement_for_current_mass + fuel_requirement_for_fuel


def main() -> None:
    """Read module masses from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    module_masses = read_module_masses(file_path)

    module_fuel_requirements = [get_module_fuel_requirement(mass) for mass in module_masses]
    print(sum(module_fuel_requirements))
    
    total_fuel_requirements = [get_total_fuel_requirement(mass) for mass in module_masses]
    print(sum(total_fuel_requirements))


if __name__ == "__main__":
    main()
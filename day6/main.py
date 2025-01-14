"""
Advent of Code 2019, Day 6
Universal Orbit Map
https://adventofcode.com/2019/day/6
"""

from dataclasses import dataclass
from os import path
from pprint import pprint
from typing import NamedTuple, Optional

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


class Orbit(NamedTuple):
    """Represents an orbital relationship between two objects."""

    parent: str
    child: str


@dataclass
class CelestialObject:
    """A celestial object in the universe."""

    def __init__(self, name: str) -> None:
        """Create a celestial object with the given name and parent."""

        self.name = name
        self.parent: Optional[CelestialObject] = None
        self.children: list[CelestialObject] = []

    def __eq__(self, other: object) -> bool:
        """Check if two celestial objects are equal by their names."""

        if not isinstance(other, CelestialObject):
            return NotImplemented

        return self.name == other.name

    def __hash__(self) -> int:
        """Hash the celestial object by its name."""

        return hash(self.name)

    def __repr__(self) -> str:
        """Return a string representation of the object."""

        return f"CelestialObject({self.name})"

    def add_orbital_child(self, child: "CelestialObject") -> None:
        """Add a child object to this object's orbit."""

        self.children.append(child)
        child.parent = self


class OrbitMap:
    """A map of celestial objects and their direct orbits."""

    def __init__(self, orbits: list[Orbit]) -> None:
        """Create an orbit map from the given orbital relationships."""

        self.celestial_objects: dict[str, CelestialObject] = {}
        for orbit in orbits:
            self.add_orbit(orbit)

    def add_orbit(self, orbit: Orbit) -> None:
        """Add an orbital relationship to the map."""

        parent_name, child_name = orbit

        parent = self.celestial_objects.get(parent_name, CelestialObject(parent_name))
        child = self.celestial_objects.get(child_name, CelestialObject(child_name))

        parent.add_orbital_child(child)

        self.celestial_objects[parent_name] = parent
        self.celestial_objects[child_name] = child

    def __getitem__(self, key: str) -> CelestialObject:
        """Get a celestial object by its name."""

        return self.celestial_objects[key]


def read_orbits(file_path: str) -> list[Orbit]:
    """Read orbital data from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_orbit(line.strip()) for line in file]


def parse_orbit(line: str) -> Orbit:
    """Parse an orbital relationship from a line of text."""

    parent, child = line.split(")")
    return Orbit(parent, child)


def get_orbit_count_checksum(celestial_object: CelestialObject) -> int:
    """Calculate the total orbit count checksum for a given celestial object."""

    def count_orbits(celestial_object: CelestialObject, depth: int) -> int:
        """Count the number of direct and indirect orbits for an object."""

        orbit_children = celestial_object.children
        children_depth = depth + 1

        return depth + sum(
            count_orbits(child, children_depth) for child in orbit_children
        )

    return count_orbits(celestial_object, 0)


# The number of transfers required would be the sum of the distances from YOU
# and SAN to the first common orbital parent, which is D in the example. So,
# we can identify all the orbital parents for each object and then find the
# first common parent between them.

# CONSIDER: An alternative structure might be warrented for this problem. The
# first part of the problem works best when the map associates parents with
# their children. However, the second works best when the map associates
# children with their parents. Ideally, we should be able to perform both
# traversals efficiently. One way we could do this is with a combination of
# a doubly-linked list and a hash map. The linked list would represent the
# direct orbits while the hash map would allow us to quickly look up
# particular objects in the map as a starting point.


def get_orbital_parents(celestial_object: CelestialObject) -> list[str]:
    """Get the orbital parents in order for a given celestial object."""

    current_object = celestial_object
    parents = []

    while current_object:
        current_object = current_object.parent
        if current_object:
            parents.append(current_object)

    return parents


def find_first_common_parent(object1: CelestialObject, object2: CelestialObject) -> str:
    """Find the first common orbital parent between two objects."""

    object1_parents = get_orbital_parents(object1)
    object2_parents = get_orbital_parents(object2)

    print(object1_parents)
    print(object2_parents)

    for parent in object1_parents:
        if parent in object2_parents:
            return parent


def get_transfer_count(origin: CelestialObject, target: CelestialObject) -> int:
    """Get the distance from a child to a parent in the orbit map."""

    transfer_count = 0
    current_object = origin.parent

    while current_object:
        if current_object == target:
            break

        current_object = current_object.parent
        transfer_count += 1

    return transfer_count


def count_transfers_to_santas_orbital_path(orbit_map: OrbitMap) -> int:
    """Count the number of orbital transfers required to reach Santa."""

    you_object = orbit_map["YOU"]
    santa_object = orbit_map["SAN"]

    common_parent = find_first_common_parent(you_object, santa_object)

    distance_from_parent_to_you = get_transfer_count(
        you_object,
        common_parent,
    )
    distance_from_parent_to_santa = get_transfer_count(
        santa_object,
        common_parent,
    )

    return distance_from_parent_to_you + distance_from_parent_to_santa


def main() -> None:
    """Read orbital data from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    orbits = read_orbits(file_path)
    print(orbits)

    orbit_map = OrbitMap(orbits)
    pprint(orbit_map)

    checksum = get_orbit_count_checksum(orbit_map["COM"])
    print(f"Total orbit count checksum: {checksum}")

    min_transfers = count_transfers_to_santas_orbital_path(orbit_map)
    print(f"Minimum orbital transfers to Santa: {min_transfers}")


if __name__ == "__main__":
    main()

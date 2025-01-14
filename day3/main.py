"""
Advent of Code 2019, Day 3
Crossed Wires
https://adventofcode.com/2019/day/3
"""

import re
from enum import Enum
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"
TEST_FILE_3 = "test3.txt"

SEGMENT_REGEX = re.compile(r"([UDLR])(\d+)")


class Position(NamedTuple):
    """Represents a position on a 2D grid relative to an origin point."""

    x: int
    y: int


class Direction(Enum):
    """Represents a direction in which a wire moves."""

    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


class Segment(NamedTuple):
    """Represents a segment of a wire path."""

    direction: Direction
    length: int


Wire = list[Segment]


def read_wires(file_path: str) -> list[Wire]:
    """Read wire data from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_wire(line) for line in file]


def parse_wire(line: str) -> Wire:
    """Parse a line of wire data into a wire path."""

    return [parse_segment(segment) for segment in line.split(",")]


def parse_segment(segment: str) -> Segment:
    """Parse a segment of a wire path."""

    pattern_match = SEGMENT_REGEX.match(segment)
    if not pattern_match:
        raise ValueError(f"Invalid segment: {segment}")

    direction = Direction(pattern_match.group(1))
    length = int(pattern_match.group(2))

    return Segment(direction, length)


def advance_position(position: Position, direction: Direction) -> Position:
    """Advance a position in a given direction."""

    x, y = position

    if direction == Direction.UP:
        return Position(x, y + 1)
    elif direction == Direction.DOWN:
        return Position(x, y - 1)
    elif direction == Direction.LEFT:
        return Position(x - 1, y)
    elif direction == Direction.RIGHT:
        return Position(x + 1, y)

    raise ValueError(f"Invalid direction: {direction}")


def get_distinct_wire_positions(wire: Wire) -> set[Position]:
    """Find the distinct positions occupied by a wire path."""

    current_position = Position(0, 0)
    visited_positions = set()

    for direction, length in wire:
        for _ in range(length):
            current_position = advance_position(current_position, direction)
            visited_positions.add(current_position)

    return visited_positions


def find_intersections(wires: list[Wire]) -> set[Position]:
    """Find the positions where two wires intersect."""

    wire_positions = [get_distinct_wire_positions(wire) for wire in wires]

    return set.intersection(*wire_positions)


def manhattan_distance(position1: Position, position2: Position) -> int:
    """Calculate the Manhattan distance between two positions."""

    return abs(position1.x - position2.x) + abs(position1.y - position2.y)


def find_distance_to_closest_intersection(wires: list[Wire]) -> int:
    """Find the distance to the closest intersection of two wires."""

    intersections = find_intersections(wires)
    origin = Position(0, 0)

    return min(manhattan_distance(origin, position) for position in intersections)


def find_minimum_steps_to_wire_positions(wire: Wire) -> dict[Position, int]:
    """Find the minimum number of steps to reach each position on a wire path."""

    current_position = Position(0, 0)
    steps_to_positions = {current_position: 0}
    steps = 0

    for direction, length in wire:
        for _ in range(length):
            current_position = advance_position(current_position, direction)
            steps += 1

            if current_position not in steps_to_positions:
                steps_to_positions[current_position] = steps

    return steps_to_positions


def find_minimum_signal_delay(wires: list[Wire]) -> int:
    """Find the minimum signal delay to an intersection of two wires."""

    wire_steps = [find_minimum_steps_to_wire_positions(wire) for wire in wires]
    intersections = find_intersections(wires)

    min_signal_delay = float("inf")

    for position in intersections:
        signal_delays = [wire_steps[position] for wire_steps in wire_steps]
        min_signal_delay = min(min_signal_delay, sum(signal_delays))

    return min_signal_delay


def main() -> None:
    """Read the paths of the two wires from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    wires = read_wires(file_path)
    print(wires)

    distance_to_closest_intersection = find_distance_to_closest_intersection(wires)
    print(distance_to_closest_intersection)

    min_signal_delay = find_minimum_signal_delay(wires)
    print(min_signal_delay)


if __name__ == "__main__":
    main()

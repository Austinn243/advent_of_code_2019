"""
Advent of Code 2019, Day 2
1202 Program Alarm
https://adventofcode.com/2019/day/2
"""

from collections.abc import Callable
from functools import partial
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

TARGET_OUTPUT = 19690720
TARGET_PARAMETER_RANGE = range(100)

Program = list[int]


class Parameters(NamedTuple):
    """Represents the noun and verb parameters of the program."""

    noun: int
    verb: int


class Operation(NamedTuple):
    """Represents an operation in the program state."""

    opcode: int
    size: int
    execute: Callable[[Program, int], Program]


def execute_add_operation(program: Program, instruction_pointer: int) -> Program:
    """Execute an add operation on the program state."""

    read_address_1 = program[instruction_pointer + 1]
    read_address_2 = program[instruction_pointer + 2]
    write_address = program[instruction_pointer + 3]

    value_1 = program[read_address_1]
    value_2 = program[read_address_2]

    result = value_1 + value_2

    updated_program = program.copy()
    updated_program[write_address] = result

    return updated_program


def execute_multiply_operation(program: Program, instruction_pointer: int) -> Program:
    """Execute a multiply operation on the program state."""

    read_address_1 = program[instruction_pointer + 1]
    read_address_2 = program[instruction_pointer + 2]
    write_address = program[instruction_pointer + 3]

    value_1 = program[read_address_1]
    value_2 = program[read_address_2]

    result = value_1 * value_2

    updated_program = program.copy()
    updated_program[write_address] = result

    return updated_program


ADD_OPERATION = Operation(opcode=1, size=4, execute=execute_add_operation)
MULTIPLY_OPERATION = Operation(opcode=2, size=4, execute=execute_multiply_operation)
HALT_OPERATION = Operation(opcode=99, size=1, execute=id)

OPERATIONS = {
    ADD_OPERATION.opcode: ADD_OPERATION,
    MULTIPLY_OPERATION.opcode: MULTIPLY_OPERATION,
    HALT_OPERATION.opcode: HALT_OPERATION,
}


def read_program_state(file_name: str) -> Program:
    """Read the initial state of the program from a file."""

    with open(file_name, encoding="utf-8") as file:
        return [int(value) for value in file.read().split(",")]


def set_program_parameters(program: Program, noun: int, verb: int) -> Program:
    """Set the noun and verb values in the program state."""

    configured_program = program.copy()

    configured_program[1] = noun
    configured_program[2] = verb

    return configured_program


recreate_1202_program_alarm_state = partial(set_program_parameters, noun=12, verb=2)


def simulate_program(program: Program) -> Program:
    """Simulate the program execution, returning the final state."""

    pointer = 0

    while True:
        operation = OPERATIONS.get(program[pointer], HALT_OPERATION)
        if operation == HALT_OPERATION:
            break

        program = operation.execute(program, pointer)
        pointer += operation.size

    return program


def read_output(program: Program) -> int:
    """Read the output value from the program state."""

    return program[0]


def parameters_yield_target_output(
    program: Program,
    parameters: Parameters,
    target_output: int,
) -> bool:
    """Determine if the given parameters produce the target output."""

    noun, verb = parameters
    configured_program = set_program_parameters(program, noun, verb)

    final_state = simulate_program(configured_program)

    output = read_output(final_state)

    return output == target_output


def find_parameters_for_output(program: Program, target_output: int) -> Parameters:
    """Find the noun and verb that produce the target output."""

    for noun in TARGET_PARAMETER_RANGE:
        for verb in TARGET_PARAMETER_RANGE:
            parameters = Parameters(noun, verb)
            if parameters_yield_target_output(program, parameters, target_output):
                return parameters

    raise ValueError("No parameters yield the target output.")


def main() -> None:
    """Read the initial program state from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    program = read_program_state(file_path)

    alarm_state = recreate_1202_program_alarm_state(program)
    final_alarm_state = simulate_program(alarm_state)
    alarm_state_output = read_output(final_alarm_state)
    print(f"The output of the recreated alarm state program is {alarm_state_output}")

    noun, verb = find_parameters_for_output(program, TARGET_OUTPUT)
    print(f"The noun and verb that produce the target output are {noun} and {verb}")
    print(f"The answer is {100 * noun + verb}")


if __name__ == "__main__":
    main()

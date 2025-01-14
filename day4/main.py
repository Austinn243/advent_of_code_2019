"""
Advent of Code 2019, Day 4
Secure Container
https://adventofcode.com/2019/day/4
"""

from collections import Counter
from collections.abc import Callable, Generator
from itertools import pairwise
from math import log10

PASSWORD_RANGE = range(359282, 820401)


Validator = Callable[[int], bool]


def get_password_length(password: int) -> int:
    """Get the length of a password."""

    return int(log10(password)) + 1


def get_nth_digit(password: int, n: int) -> int:
    """Get the nth digit of a password."""

    return password // 10**n % 10


def get_digits_by_significance(password: int) -> Generator[int, None, None]:
    """Get the digits of a password starting from the most significant digit."""

    password_length = get_password_length(password)

    for power in range(password_length - 1, -1, -1):
        yield get_nth_digit(password, power)


def all_digits_in_ascending_order(password: int) -> bool:
    """Check if the digits of a password are in ascending order."""

    return all(
        left_digit <= right_digit
        for left_digit, right_digit in pairwise(get_digits_by_significance(password))
    )


def contains_repeated_digits(password: int) -> bool:
    """Check if a password has two or more repeated digits."""

    return any(
        left_digit == right_digit
        for left_digit, right_digit in pairwise(get_digits_by_significance(password))
    )


def contains_isolated_pair_of_repeated_digits(password: int) -> bool:
    """Check if the password contains an isolated pair of repeated digits.

    The repeated digits must not be part of a larger group of repeated digits.
    """

    digit_counts = Counter(get_digits_by_significance(password))

    return any(count == 2 for count in digit_counts.values())


def count_valid_passwords(
    password_range: range,
    criteria: list[Validator],
) -> int:
    """Count the number of valid passwords within a password range."""

    return sum(
        all(criteria(password) for criteria in criteria) for password in password_range
    )


def main() -> None:
    """Process the range of possible passwords."""

    criteria = [
        all_digits_in_ascending_order,
        contains_repeated_digits,
    ]

    lenient_valid_password_count = count_valid_passwords(
        PASSWORD_RANGE,
        criteria,
    )

    criteria.append(contains_isolated_pair_of_repeated_digits)
    strict_valid_password_count = count_valid_passwords(
        PASSWORD_RANGE,
        criteria,
    )

    print("The number of passwords with each criteria met are")
    print(f"Lenient criteria: {lenient_valid_password_count}")
    print(f"Strict criteria: {strict_valid_password_count}")


if __name__ == "__main__":
    main()


# 156 is too low
# 202 is too low
# 261 is wrong.
# 344 is too high

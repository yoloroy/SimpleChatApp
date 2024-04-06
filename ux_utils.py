from typing import Callable, Optional


def read_until_parsed_successfully[T](title: str, parse: Callable[[str], Optional[T]]) -> T:
    parsed: T
    while not (parsed := parse(input(title))):
        print("bad input from bad user")
        print()

    return parsed


def is_ip(text: str):
    parts = text.split(".")
    return len(parts) == 4 and all(str.isdigit(part) for part in parts)

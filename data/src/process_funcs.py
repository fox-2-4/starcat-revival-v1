
import vector_math


vector = tuple[float, float, float] | list[float]


def process_main_id(__main_id: str) -> str:
    ...

def process_numeric(__val: str) -> float | None:
    ...

def process_coordinates(__coords: str, fmt: str = "x m s") -> vector:
    ...


import vector_math


vector = tuple[float, float, float] | list[float]


def process_main_id(__main_id: str) -> str:
    main_id_components = __main_id.strip().split(" ")
    while main_id_components[0] in ("*", "**", "V*", "NAME"):
        del main_id_components[0]
    return " ".join(main_id_components)

def process_numeric_val(__val: str) -> float | None:
    __val = __val.strip()
    try:
        val = float(__val)
    except ValueError:
        try:  # sometimes extracted values are appended by errant brackets, pipes, etc.
            val = float(__val[0: -1])
        except ValueError:
            return None  # could not extract float value
    return val

def process_coordinates(__coords: str, fmt: str = "x m s", sep: str = " ") -> vector | None:
    __coords = __coords.strip().split(sep)
    if len(__coords) == 0 or len(__coords) > 3:  # bad string
        return None

    coords: vector = [None, None, None]
    for i, val in enumerate(__coords):
        try:
            coords[i] = float(val)
        except ValueError:
            return None
    return coords
    

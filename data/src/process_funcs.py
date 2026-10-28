
import vector_math


vector = tuple[float, float, float] | list[float]


def parse_main_id(__main_id: str) -> str:
    main_id_components = __main_id.strip().split(" ")
    while main_id_components[0] in ("*", "**", "V*", "NAME"):
        del main_id_components[0]
    return " ".join(main_id_components)


def parse_numeric_val(__val: str) -> float | None:
    __val = __val.strip()
    try:
        val = float(__val)
    except ValueError:
        try:  # sometimes extracted values are appended by errant brackets, pipes, etc.
            val = float(__val[0: -1])
        except ValueError:
            return None  # could not extract float value
    return val


def parse_coordinates(
        __coords: str, 
        fmt: str = "x m s", 
        sep: str = " ",
        strict: bool = True
) -> vector | None:

    __coords = __coords.strip().split(sep)

    if len(__coords) == 0 or len(__coords) > 3:  # bad string
        return None

    coords: vector = [0.0, 0.0, 0.0]

    # With 'strict', parsing returns 'None' if any of the coordinate commponents is omitted or otherwise can't be parsed.
    # This ends up excluding most "groups" of objects (ex., "Ursa Major Moving Group"). 
    if strict:
        for i, val in enumerate(__coords):
            try:
                coords[i] = float(val)
            except ValueError:
                return None
    
    # With 'strict' set to 'False', group objects can be included if at least the primary degree of measure or better
    # can be parsed, i.e., the hours/degrees measurement. The other higher-precision elements are set to 0.0.
    # Has the potential side effect of passing erroneous data. 
    else:
        for i, val in enumerate(__coords):
            try:
                coords[i] = float(val)
            except ValueError:
                if i == 0: return None  # primary element of the coordinates could be resolved
                return coords  # return early, higher precision measurements = 0.0
    
    return coords
                

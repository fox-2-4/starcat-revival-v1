import math


vector = tuple[float, float, float] | list[float]


def sign(x):
    return (x > 0) - (x < 0)  # `bool` is a subclass of `int`

def hms_to_radians(hms: vector) -> float:
    return (hms[0] * 15 + hms[1] / 4 + hms[0] / 240) * math.pi / 180

def dms_to_radians(dms: vector) -> float:
    return ((abs(dms[0]) + dms[1] / 60 + dms[2] / 3600) * sign(dms[0])) * math.pi / 180

def mas_to_radians(mas: float) -> float:
    return mas / 2.062648062471e+8

def radians_to_hms(a):
    x = a * 180 / math.pi  # convert radians to degrees
    h = x / 360 * 24
    m = (h - math.floor(h)) * 60
    s = (m - math.floor(m)) * 60
    return int(h), int(m), s

def radians_to_dms(b):
    x = b * 180 / math.pi
    d = x
    m = (abs(d) - math.floor(abs(d))) * 60
    s = (m - math.floor(m)) * 60
    return int(d), int(m), s

def equatorial_to_spherical(vec: vector) -> vector:
    """
    Converts Equatorial Coordinate System radian values to standard ISO spherical coordinates.
    :param vec: tuple containing: ECS right ascension [0, 2pi]; ECS declination [-pi/2, +pi/2]; distance measurement.
    :return: Standard ISO spherical: distance, theta (0, pi], phi [-pi, +pi]. 
    """
    ra, dec, d = vec
    return d, dec + math.pi / 2, ra - math.pi

def spherical_to_cartesian(vec: vector) -> vector:
    """
    Converts ISO standard spherical coordinates (radius, theta, phi) to cartesian (x, y, z). 
    :param vec: tuple containing: radial "stant" distance; polar angle from zenith; and azimuthal angle of rotation.
    :return: Cartesian (x, y, z) spatial coordinates. 
    """
    r, theta, phi = vec
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    return x, y, z

def cartesian_to_spherical(pt: vector) -> vector:
    """
    Converts Cartesian coordinates (x, y, z) to standard ISO spherical (r, theta, phi).
    :param pt: Cartesian point (x, y, z) w/ implicit origin (0, 0, 0).
    :return: ISO spherical coordinates (r, theta, phi); or `None` as "undefined" (point coincides w/ origin).
    """
    x, y, z = pt
    xy_sqrsum = x**2 + y**2
    r = math.sqrt(xy_sqrsum + z**2)
    if r == 0.0:  # unit sphere radius zero, vector direction undefined
        return None
    elif xy_sqrsum == 0.0:  # xy-projected r is zero, vector points straight up/down
        return r, sign(z) * math.radians(90) + math.radians(90), 0.0
    # -- no division errors beyond this point --
    try:
        theta = math.acos(z / r)
        phi = sign(y) * math.acos(x / math.sqrt(xy_sqrsum))
    except ValueError:  # this will have to be the result of math.acos and requires further debugging
        return None

    return r, theta, phi

def distance(pt0: vector, pt1: vector) -> float | None:
    return math.sqrt(
        (pt0[0] - pt1[0]) ** 2 + 
        (pt0[1] - pt1[1]) ** 2 + 
        (pt0[2] - pt1[2]) ** 2
    )

def rotate_on_x_axis(pt: vector, theta: float) -> vector:
    if theta == 0.0:
        return pt
    return [pt[0],
            pt[1] * math.cos(theta) - pt[2] * math.sin(theta),
            pt[1] * math.sin(theta) + pt[2] * math.cos(theta)]

def rotate_on_y_axis(pt: vector, theta: float) -> vector:
    if theta == 0.0:
        return pt
    return [pt[0] * math.cos(theta) + pt[2] * math.sin(theta),
            pt[1],
            pt[2] * math.cos(theta) - pt[0] * math.sin(theta)]

def rotate_on_z_axis(pt: vector, theta: float) -> vector:
    if theta == 0.0:
        return pt
    return [pt[0] * math.cos(theta) - pt[1] * math.sin(theta),
            pt[0] * math.sin(theta) + pt[1] * math.cos(theta),
            pt[2]]
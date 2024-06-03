import gpxpy
from math import radians, acos, cos, sin, atan2, degrees
import os

# latitude = zemepisna sirka
# longitude = zemepisna delka

MESSAGES = [
    "{pt1.name} >> {pt2.name}: Azimuth = {azim:.2f}° & Distance = {dist:.2f} m",
    "{pt1.name} >> {pt2.name}: {azim:.2f}° {dist:.2f} m",
]
# zprava se pouziva vsude mozne
MESSAGE = MESSAGES[1]


class Point:
    def __init__(self, name, latitude, longitude) -> None:
        self.name: str = name
        self.latitude: float = float(latitude)
        self.longitude: float = float(longitude)

    def __str__(self) -> str:
        return f"{self.name}: {self.latitude}N, {self.longitude}E"


def gpx_parse_to_list(path: str) -> list[Point]:
    res: list[Point] = []

    try:
        with open(path, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for wpt in gpx.waypoints:
                name = wpt.name
                latitude = wpt.latitude
                longitude = wpt.longitude
                point: Point = Point(name, latitude, longitude)
                res.append(point)
    except Exception as e:
        print(f"Error parsing GPX file: {e}")

    return res


def gpx_parse_str_to_list(string: str) -> list[Point]:
    res: list[Point] = []

    try:
        gpx = gpxpy.parse(string)
        for wpt in gpx.waypoints:
            name = wpt.name
            latitude = wpt.latitude
            longitude = wpt.longitude
            point: Point = Point(name, latitude, longitude)
            res.append(point)

        resSTR: list[str] = []

        for i in range(len(res) - 1):
            pt1, pt2 = res[i], res[i + 1]
            azim = calculate_azimuth(pt1, pt2)
            dist = calculate_distance(pt1, pt2) * 1000
            resSTR.append(MESSAGE.format(pt1=pt1, pt2=pt2, azim=azim, dist=dist))

        return resSTR

    except Exception as e:
        print(f"Error parsing GPX string: {e}")

    return [
        "Došlo k chybě.",
        "Nejspíš máte poškozený soubor.",
        "Zkuste mapu exportovat znovu a pak ji sem znovu nahrát.",
    ]


def calculate_azimuth(pt1: Point, pt2: Point) -> float:
    lat1, lon1 = radians(pt1.latitude), radians(pt1.longitude)
    lat2, lon2 = radians(pt2.latitude), radians(pt2.longitude)

    dLon = lon2 - lon1

    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)

    brng = atan2(y, x)
    brng = degrees(brng)

    azimuth = 360.0 + brng
    azimuth %= 360.0

    return azimuth


def calculate_distance(pt1: Point, pt2: Point) -> float:
    mlat, plat = radians(pt1.latitude), radians(pt2.latitude)
    mlon, plon = radians(pt1.longitude), radians(pt2.longitude)
    dist = 6371.01 * acos(
        sin(mlat) * sin(plat) + cos(mlat) * cos(plat) * cos(mlon - plon)
    )
    return dist


def print_list(list_points: list[Point]):
    for i in range(len(list_points) - 1):
        pt1, pt2 = list_points[i], list_points[i + 1]
        azim = calculate_azimuth(pt1, pt2)
        dist = calculate_distance(pt1, pt2)
        print(MESSAGE.format(pt1=pt1, pt2=pt2, azim=azim, dist=dist))


def parse_file(path: str):
    list_points = gpx_parse_to_list(path)
    print_list(list_points)


def parse_folder(dir: str):
    paths = os.listdir(dir)

    for path in paths:
        path = os.path.join(dir, path)
        print(f"Instructions for {path}")
        parse_file(path)
        print()

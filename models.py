from typing import NamedTuple

class Location(NamedTuple):
    latitude: str
    longitude: str

class Metadata(NamedTuple):
    createDate: str
    location: Location


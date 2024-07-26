from dataclasses import dataclass
from enum import Enum


class Shape(Enum):
    OVAL = 1
    DIAMOND = 2
    SQUIGGLE = 3


class Filling(Enum):
    OPEN = 1
    SHADED = 2
    STRIPED = 3


class Numbers(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class Color(Enum):
    RED = 1
    PURPLE = 2
    GREEN = 3


@dataclass(frozen=True)
class Card:
    shape: Shape
    number: Numbers
    filling: Filling
    color: Color
    id: int

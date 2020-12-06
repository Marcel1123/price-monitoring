import enum


class ProductType(enum.Enum):
    DETACHED = 0
    SEMI_DETACHED = 1
    NON_DETACHED = 2
    STUDIO = 3
    HOUSE = 4
    NULL = 5

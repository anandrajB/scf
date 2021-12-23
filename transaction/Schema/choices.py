import graphene


class financeType(graphene.Enum):
    AUTOMATIC = "AUTOMATIC"
    ON_REQUEST = "ON_REQUEST"


class interestType(graphene.Enum):
    FIXED = "FIXED"
    FLOATING = "FLOATING"


class interestRate(graphene.Enum):
    LIBOR = "LIBOR"
    EURIBOR = "EURIBOR"
    SOFOR = "SOFOR"

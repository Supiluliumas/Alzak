from enum import Enum, auto


class SimEvent(Enum):
    JUMPED = auto()
    LANDED = auto()
    LASER_STARTED = auto()
    LASER_STOPPED = auto()
    LASER_OVERHEATED = auto()
    ENEMY_HIT = auto()
    ENEMY_DEFEATED = auto()
    EXIT_ACTIVATED = auto()
    PLAYER_HURT = auto()
    PLAYER_FELL = auto()
    PLAYER_DEFEATED = auto()
    LEVEL_COMPLETED = auto()

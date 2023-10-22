from dataclasses import dataclass


@dataclass
class Match:
    id: int
    name: str
    status: str
    map: str


@dataclass
class Player:
    id: int
    name: str


@dataclass
class PlayerMatchData(Player):
    side: str

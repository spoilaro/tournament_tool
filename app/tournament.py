
from dataclasses import dataclass


@dataclass
class Player():
    name: str


class Tournament:
    def __init__(self):
        self.map = "Mirage"

        self.players: list[Player] = []

        self.options = {}

    def add_players(self):
        while True:
            name = input("Player: ")

            if not name:
                return

            player = Player(name=name)
            self.players.append(player)


if __name__ == "__main__":
    tournament = Tournament()

    tournament.add_players()


import logging
import sqlite3
from uuid import uuid4

log = logging.getLogger(__name__)


def create_connection():
    conn = sqlite3.connect("db/tournament_tool.db", check_same_thread=False)
    return conn


conn = create_connection()


class Tournament:
    def __init__(self):
        pass

    def check_active_tournament(self):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT tournament_id FROM tournaments WHERE tournament_status = 'ONGOING'")

        tournament = cursor.fetchone()

        if not tournament:
            print("NO ACTIVE TOURNAMENT")
            return None

        return tournament[0]

    def init_players(self, tour_id):
        cursor = conn.cursor()

        with open("players.txt") as f:
            for conf in f.readlines():

                name = conf.split(" ")[0].replace("\n", "")
                cursor.execute(
                    """
                        INSERT INTO players (player_name, tournament_id) VALUES (?, ?)
                    """, (name, tour_id))
                conn.commit()

    def init_options(self, tournament_id):
        cursor = conn.cursor()

        cursor.execute("""
                INSERT INTO tournament_options (
                    tournament_id,
                    map,
                    time_limit
                ) VALUES (
                    ?,
                    1,
                    120
                )
                """, (tournament_id, ))
        conn.commit()

    def init_matches(self, tour_id):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT player_id FROM players WHERE tournament_id = ?", (tour_id, ))

        players = cursor.fetchall()
        match_count = int(len(players) / 2)

        print(f"PLAYER COUNT: {len(players)}")
        print(f"MATCH COUNT: {match_count}")

        ct_side = [p[0] for p in players[:match_count]]
        t_side = [p[0] for p in players[match_count:]]

        for pair in range(match_count):

            match_name = f"{ct_side[pair]} VS {t_side[pair]}"
            match_id = str(uuid4())
            cursor.execute("""
                INSERT INTO matches (
                    match_id,
                    match_name,
                    map_id,
                    tournament_id
                ) VALUES (
                    ?,
                    ?,
                    1,
                    ?
                )
            """, (match_id, match_name, tour_id))
            conn.commit()

            params = [
                (match_id, ct_side[pair], "CT"),
                (match_id, t_side[pair], "T")
            ]

            cursor.executemany("""
                INSERT INTO players_in_matches (
                    match_id,
                    player_id,
                    side
                ) VALUES
                    (?, ?, ?)
            """, params)
            conn.commit()

    def activate_tournament(self, tour_id):
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE tournaments SET tournament_status = 'ONGOING' WHERE tournament_id = ?", (tour_id, ))
        conn.commit()

    def init(self):
        cursor = conn.cursor()

        tour_id = str(uuid4())

        cursor.execute(
            "INSERT INTO tournaments (tournament_id, tournament_name) VALUES (?, 'DEMO TOURNAMENT')", (tour_id, ))
        conn.commit()

        self.init_options(tour_id)
        self.init_players(tour_id)
        self.init_matches(tour_id)
        self.activate_tournament(tour_id)


if __name__ == "__main__":
    tournament = Tournament()

    tournament.init()

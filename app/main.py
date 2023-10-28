from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

from app.data import Match, Player, PlayerMatchData

app = FastAPI()
app.mount('/templates', StaticFiles(directory='templates'), name='templates')


templates = Jinja2Templates(directory="templates")


def create_connection():
    conn = sqlite3.connect("db/tournament_tool.db", check_same_thread=False)
    return conn


def get_matches() -> list[Match]:

    conn = create_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            m.match_id,
            m.match_name,
            m.status,
            ma.map_name
        FROM
            matches m,
            maps ma
        WHERE
            m.map_id = ma.map_id
        """
    cursor.execute(query)
    matches = cursor.fetchall()

    conn.close()

    return [Match(id=m[0], name=m[1], status=m[2], map=m[3]) for m in matches]


def get_players_in_match(match_id: str) -> list[Player]:

    conn = create_connection()
    cursor = conn.cursor()
    query = """
                SELECT
                    pm.player_id as player_id,
                    pm.side as side,
                    p.player_name as player_name
                FROM
                    players_in_matches pm,
                    players p
                WHERE pm.match_id = ?
                AND p.player_id = pm.player_id
            """
    cursor.execute(query, (match_id, ))

    all_players = [PlayerMatchData(id=p[0], name=p[2], side=p[1])
                   for p in cursor.fetchall()]

    print(all_players)

    ct = []
    t = []
    for p in all_players:
        if p.side == "CT":
            ct.append(p)
        else:
            t.append(p)

    conn.close()
    return {"ct": ct, "t": t}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):

    return templates.TemplateResponse("index.html", {
        "request": request, "matches": get_matches()
    })


@app.get("/init", response_class=HTMLResponse)
def root(request: Request):

    return templates.TemplateResponse("create_tournament.html", {
        "request": request
    })


@ app.get("/match")
async def get_match(request: Request, match_id: str = None):

    conn = create_connection()
    cursor = conn.cursor()
    query = """
                SELECT
                    m.match_id,
                    m.match_name,
                    m.status,
                    ma.map_name
                FROM
                    matches m,
                    maps ma
                WHERE
                    match_id = ?
                    AND
                    m.map_id = ma.map_id
            """

    cursor.execute(query, (match_id,))
    raw_match = cursor.fetchone()
    match = Match(id=raw_match[0], name=raw_match[1], status=raw_match[2], map=raw_match[3])

    return templates.TemplateResponse("match_data.html", {
        "request": request,
        "match": match,
        "players": get_players_in_match(match.id)
    })

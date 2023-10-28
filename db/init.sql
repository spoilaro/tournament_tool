CREATE TABLE tournaments (
	tournament_id UUID PRIMARY KEY,
	tournament_name TEXT,
	tournament_status TEXT DEFAULT "NOT_STARTED"
);

CREATE TABLE tournament_options (
	option_id INTEGER PRIMARY KEY AUTOINCREMENT,
	tournament_id UUID NOT NULL,
	map INTEGER NOT NULL,
	time_limit INTEGER NOT NULL
);

CREATE TABLE players (
	player_id INTEGER PRIMARY KEY AUTOINCREMENT,
	player_name TEXT,
	tournament_id UUID NOT NULL,
	FOREIGN KEY(tournament_id) REFERENCES tournaments(tournament_id)
);

CREATE TABLE matches (
	match_id UUID PRIMARY KEY,
	match_name TEXT,
	status TEXT DEFAULT "NOT_STARTED",
	map_id INTEGER NOT NULL,
	tournament_id UUID NOT NULL,
	FOREIGN KEY(map_id) REFERENCES maps(map_id),
	FOREIGN KEY(tournament_id) REFERENCES tournaments(tournament_id)
);

CREATE TABLE players_in_matches (
	match_id UUID NOT NULL,
	player_id INTEGER NOT NULL,
	side TEXT NOT NULL,
	FOREIGN KEY(match_id) REFERENCES matches(match_id),
	FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE TABLE maps (
	map_id INTEGER PRIMARY KEY AUTOINCREMENT,
	map_name TEXT
);


-- Demo Maps
INSERT INTO maps (map_name) values ("Dust II");


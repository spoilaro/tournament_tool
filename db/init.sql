CREATE TABLE players (
	player_id INTEGER PRIMARY KEY AUTOINCREMENT,
	player_name TEXT
);

CREATE TABLE matches (
	match_id INTEGER PRIMARY KEY AUTOINCREMENT,
	match_name TEXT,
	status TEXT DEFAULT "ONGOING",
	map_id INTEGER NOT NULL,
	FOREIGN KEY(map_id) REFERENCES maps(map_id)
);

CREATE TABLE players_in_matches (
	match_id INTEGER NOT NULL,
	player_id INTEGER NOT NULL,
	side TEXT NOT NULL,
	FOREIGN KEY(match_id) REFERENCES matches(match_id),
	FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE TABLE maps (
	map_id INTEGER PRIMARY KEY AUTOINCREMENT,
	map_name TEXT
);


-- Demo players
INSERT INTO players (player_name) values ("GetRight");
INSERT INTO players (player_name) values ("Simple");
INSERT INTO players (player_name) values ("Spoilar");
INSERT INTO players (player_name) values ("Some");

-- Demo Maps
INSERT INTO maps (map_name) values ("Dust II");

-- Demo matches
INSERT INTO matches (match_name, map_id) values ("GetRight VS Simple", 1);
INSERT INTO matches (match_name, status, map_id) values ("Spoilar VS Some", "OVER", 1);

-- Demo players in matches
-- Match 1
INSERT INTO players_in_matches (match_id, player_id, side) values (1, 1, "T"); -- GetRight
INSERT INTO players_in_matches (match_id, player_id, side) values (1, 2, "CT"); -- Simple
INSERT INTO players_in_matches (match_id, player_id, side) values (1, 3, "T"); -- Spoilar
INSERT INTO players_in_matches (match_id, player_id, side) values (1, 4, "CT"); -- Some

-- Match2
INSERT INTO players_in_matches (match_id, player_id, side) values (2, 3, "T"); -- Spoilar
INSERT INTO players_in_matches (match_id, player_id, side) values (2, 4, "CT"); -- Some

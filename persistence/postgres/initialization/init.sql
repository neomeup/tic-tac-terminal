CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    account_user TEXT NOT NULL,
    player_type TEXT NOT NULL,
    agent_name TEXT,
    agent_version TEXT,
    policy_name TEXT,
    policy_version TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE simulation_runs (
    id SERIAL PRIMARY KEY,
    sim_uuid TEXT NOT NULL,
    batch_id INTEGER NOT NULL,
    rule_set TEXT NOT NULL,
    encoder TEXT NOT NULL,
    reward_system_player_1 TEXT NOT NULL,
    reward_system_player_2 TEXT NOT NULL,
    num_games INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    config_json JSONB
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    simulation_run_id INTEGER REFERENCES simulation_runs(id),
    batch_id INTEGER NOT NULL,
    player_one_id INTEGER REFERENCES players(id),
    player_two_id INTEGER REFERENCES players(id),
    winner_player_id INTEGER REFERENCES players(id),
    winner_in_game_id INTEGER,
    is_draw BOOLEAN,
    total_moves INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    simulation_run_id INTEGER REFERENCES simulation_runs(id),
    batch_id INTEGER NOT NULL,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES players(id) NULL,
    player_id_in_game INTEGER,
    turn_number INTEGER,
    row_index INTEGER,
    col_index INTEGER,
    reward FLOAT,
    board_state_json JSONB
);
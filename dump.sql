CREATE DATABASE slack;
CREATE TABLE boards(id INT NOT NULL AUTO_INCREMENT,
    player0_id VARCHAR(100) NOT NULL,
    player1_id VARCHAR(100) NOT NULL,
    player0_nickname VARCHAR(40) NOT NULL,
    player1_nickname VARCHAR(40) NOT NULL,
    player_turn VARCHAR(100) NOT NULL,
    channel_id VARCHAR(100) NOT NULL,
    state VARCHAR(9) NOT NULL,
    updated_at VARCHAR(100) NOT NULL,
    created_at VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);


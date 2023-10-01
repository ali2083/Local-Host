DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS files;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(32) UNIQUE NOT NULL,
  mac_address VARCHAR(12) UNIQUE NOT NULL
);

CREATE TABLE chats (
  user_id INTEGER NOT NULL,
  massage_text TEXT NOT NULL,
  date TIMESTAMP NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255),
  user_id INTEGER NOT NULL,
  date TIMESTAMP NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    bar_name TEXT NOT NULL,
    bar_address TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    happy_hour BOOLEAN DEFAULT 0,
    student_discount BOOLEAN DEFAULT 0,
    gluten_free BOOLEAN DEFAULT 0,
    student_patch BOOLEAN DEFAULT 0,
    extra_info TEXT
);

CREATE TABLE drink (
    id INTEGER PRIMARY KEY,
    drink_name TEXT NOT NULL UNIQUE -- beer, lonkero, jne
);

CREATE TABLE price(
    id INTEGER PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    drink_id INTEGER REFERENCES drink(id),
    drink_size TEXT NOT NULL, -- should be 0.33, 0.5
    price REAL NOT NULL
);

CREATE TABLE comments(
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users(id), 
    location_id INTEGER REFERENCES locations(id)
);

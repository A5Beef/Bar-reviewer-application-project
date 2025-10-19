-- USERS
INSERT INTO users (username, password_hash) VALUES ('Barhater', 'alkomaholitappaa');
INSERT INTO users (username, password_hash) VALUES ('Beerlover', 'kaljamielessa24');
INSERT INTO users (username, password_hash) VALUES ('Alcohol_free221', '0percentchanceofdrinking');
INSERT INTO users (username, password_hash) VALUES ('Maija_Miettinen', 'Maija1234');
INSERT INTO users (username, password_hash) VALUES ('troll67', 'sixseven');

-- DRINKS
INSERT INTO drink (drink_name) VALUES ('beer');
INSERT INTO drink (drink_name) VALUES ('lonkero');
INSERT INTO drink (drink_name) VALUES ('ananas');
INSERT INTO drink (drink_name) VALUES ('cider');

-- LOCATIONS
INSERT INTO locations (bar_name, bar_address, user_id, happy_hour, student_discount, gluten_free, student_patch, extra_info)
VALUES 
('ALCOHOL KILLS', 'Alkoholi tappaa', 1, 0, 0, 0, 0, 'HATE ALCOHOL STOP DRINKING!!!'),
('Baarin niminen baari', 'Baarikuja 14', 3, 1, 1, 0, 0, 'Normal bar... they have lemonade lonkero on tap. Pepsi and Jaffa on tap... Mocktails are awesome...'),
('5 STAR BAR', 'i dont remember', 5, 1, 1, 1, 1, 'just kidding this place doesnt exist'),
('Mascot Bar & Live Stage', 'Neljäs linja 2', 4, 0, 0, 1, 1, 'Not sure about prices dont remember. Karaoke place its so nice. They have a private karaoke booth!'),
('Vivian''s Kitchen Bar', 'Kustaankatu 4', 4, 1, 0, 1, 1, 'Ihan kiva haalarimerkki, Kukkoa löytyy gluteenittomana. Hyvät hinnat! Student''s favourite! Hartwall taps. They have flavoured soju! Very cool! HYVÄÄ MUSAA');

-- PRICES

-- Bar Two
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 1, '0.33/0.4', 6.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 1, '0.5', 8.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 2, '0.33', 7.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 2, '0.5', 9.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 3, '0.33', 7.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 3, '0.5', 9.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 4, '0.33', 7.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (2, 4, '0.5', 9.0);
-- Bar Three
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 1, '0.33/0.4', 99999.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 1, '0.5', 999999.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 2, '0.33', 12345.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 2, '0.5', 67.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 3, '0.33', 67.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 3, '0.5', 67.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 4, '0.33', 912380.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (3, 4, '0.5', 1337.0);
-- Bar Four
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (4, 1, '0.33/0.4', 5.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (4, 2, '0.33', 6.20);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (4, 3, '0.33', 6.20);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (4, 4, '0.33', 6.20);
-- Bar Five
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (5, 1, '0.5', 5.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (5, 2, '0.33', 6.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (5, 3, '0.33', 6.0);
INSERT INTO price (location_id, drink_id, drink_size, price) VALUES (5, 4, '0.33', 6.0);


-- Comments on location 1
INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Bro why are you here', CURRENT_TIMESTAMP, 2, 1);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Have you considered nonalcoholic drinks', CURRENT_TIMESTAMP, 3, 1);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('BEFORE YOU COMPLAIN TRY GETTING DRUNK LMFAO', CURRENT_TIMESTAMP, 5, 1);

-- Comment ON LOCATION 2
INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Beer...... <3', CURRENT_TIMESTAMP, 2, 2);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('A normal bar for normal people like me i love normality', CURRENT_TIMESTAMP, 4, 2);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('WHAT IS THIS PLACE', CURRENT_TIMESTAMP, 5, 2);

-- Comment location 3
INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('...beer? ..............99999..............', CURRENT_TIMESTAMP, 2, 3);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('This is how much alcohol should really cost. Good job.', CURRENT_TIMESTAMP, 1, 3);

-- commente location4
INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Also lots of crowd and 2 floors amazing good vibes drinks are flowing', CURRENT_TIMESTAMP, 4, 4);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Beer!', CURRENT_TIMESTAMP, 2, 4);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Amazing vibes wow so nice mocktailssssssssssssssssss', CURRENT_TIMESTAMP, 3, 4);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('No troll this place is lit!!!! fire', CURRENT_TIMESTAMP, 5, 4);

-- commente location5
INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('Forgot to mention but very cozy, nice music and awesome bartenders', CURRENT_TIMESTAMP, 4, 5);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('BEER!!!!!!!! HAPPYHOUR 4.50!!!!!!!!!', CURRENT_TIMESTAMP, 2, 5);

INSERT INTO comments (content, sent_at, user_id, location_id)
VALUES ('i hate alcohol.', CURRENT_TIMESTAMP, 1, 5);


import db


def add_location(bar_name, bar_address, user_id, happy_hour, student_discount, gluten_free, student_patch, extra_info):
    sql= """INSERT INTO locations
      (bar_name, bar_address, user_id, happy_hour, student_discount, gluten_free, student_patch, extra_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [bar_name, bar_address, user_id, happy_hour, student_discount, gluten_free, student_patch, extra_info])
    location_id = db.last_insert_id()
    #add drink...? price..?
    return location_id

def add_comment(content, user_id, location_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, location_id)
    VALUES (?, datetime("now"), ?, ?)"""
    db.execute(sql, [content, user_id, location_id])

def add_drink(drink_name):
    # Check
    existing = db.query("SELECT id FROM drink WHERE drink_name = ?", [drink_name])
    if existing:
        return existing[0][0]
    
    # NEW DRINK
    sql = "INSERT INTO drink (drink_name) VALUES (?)"
    db.execute(sql, [drink_name])
    return db.last_insert_id()

def add_price(location_id, drink_id, drink_size, price):
    sql =  """INSERT INTO price
    (location_id, drink_id, drink_size, price) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [location_id, drink_id, drink_size, price])

def update_drink_price(location_id, drink_id, drink_size, new_price):
    sql = """UPDATE price
    SET price = ? 
    WHERE location_id = ? 
    AND drink_id = ? 
    AND drink_size = ?"""
    db.execute(sql, [new_price, location_id, drink_id, drink_size])

def get_locations():
    sql = """SELECT l.id, l.bar_name, l.bar_address,
    COUNT(c.id) total, MAX(c.sent_at) last
    FROM locations l
    LEFT JOIN comments c ON l.id = c.location_id
    GROUP BY l.id
    ORDER BY l.id DESC"""
    return db.query(sql)


def get_location(location_id):
    sql ="""SELECT id, bar_name, bar_address, happy_hour, student_discount,
     gluten_free, student_patch, extra_info FROM locations WHERE id = ? """
    return db.query(sql, [location_id])[0]

def get_comments(location_id):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
    FROM comments c, users u
    WHERE c.user_id = u.id AND c.location_id = ?
    ORDER BY c.id"""
    return db.query(sql, [location_id])


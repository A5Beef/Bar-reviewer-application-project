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

    existing = db.query("SELECT id FROM price WHERE location_id=? AND drink_id=? AND drink_size=?",
                         [location_id, drink_id, drink_size])
    if existing:
        sql = """UPDATE price
                 SET price=? 
                 WHERE location_id=? AND drink_id=? AND drink_size=?"""
        db.execute(sql, [price, location_id, drink_id, drink_size])

    else:
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

def get_drinks(location_id):
    sql = """SELECT d.id, d.drink_name, p.drink_size, p.price
    FROM drink d
    JOIN price p ON p.drink_id = d.id
    WHERE p.location_id = ?
    ORDER BY d.drink_name ASC"""
    return db.query(sql, [location_id])

def get_comments(location_id):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
    FROM comments c, users u
    WHERE c.user_id = u.id AND c.location_id = ?
    ORDER BY c.id"""
    return db.query(sql, [location_id])

def get_comment(comment_id):
    sql = "SELECT id, content, user_id, location_id FROM comments WHERE id = ?"
    return db.query(sql, [comment_id])[0]

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def search(query):
    sql = """SELECT 
                l.id as location_id,
                l.bar_name as location_name,
                NULL as username,
                NULL as sent_at,
                'location' as match_type
             FROM locations l
             WHERE l.bar_name LIKE '%' || ? || '%'
             
             UNION
             
             SELECT 
                c.location_id,
                l.bar_name,
                u.username,
                c.sent_at,
                'comment' as match_type
             FROM comments c
             JOIN locations l ON c.location_id = l.id
             JOIN users u ON c.user_id = u.id
             WHERE c.content LIKE '%' || ? || '%'
             
             ORDER BY location_name"""
    return db.query(sql, [query, query])


def update_location(location_id, bar_name, bar_address, happy_hour,
                    student_discount, gluten_free, student_patch, extra_info):
    
    sql = """UPDATE locations
            SET bar_name=?, bar_address=?, happy_hour=?, student_discount=?, gluten_free=?, student_patch=?, extra_info=?
            WHERE id=?"""
    db.execute(sql, [bar_name, bar_address, happy_hour, student_discount,
                     gluten_free, student_patch, extra_info, location_id])

def remove_location(location_id):
    sql_comments="""DELETE FROM comments WHERE location_id = ?"""
    db.execute(sql_comments, [location_id])

    sql_prices= """DELETE FROM price
    WHERE location_id = ?"""
    db.execute(sql_prices, [location_id])

    sql_drinks= """DELETE FROM drink
    WHERE id NOT IN (SELECT DISTINCT drink_id
    FROM price)"""
    db.execute(sql_drinks)

    sql = """DELETE FROM locations WHERE id = ?"""
    db.execute(sql, [location_id])



def get_creator(location_id):
    sql = """SELECT u.id, u.username 
         FROM users u
         JOIN locations l ON u.id = l.user_id
         WHERE l.id = ?"""
    result = db.query(sql, [location_id])
    return result[0] if result else None
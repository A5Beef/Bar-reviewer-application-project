import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"  
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_comments(user_id):
    sql = """SELECT c.id,
                    c.location_id,
                    l.bar_name as location_name, 
                    c.sent_at,
                    c.content 
             FROM comments c
             JOIN locations l ON l.id = c.location_id
             WHERE c.user_id = ?
             ORDER BY c.sent_at DESC"""
    return db.query(sql, [user_id])



#testing

def get_locations(user_id):
    sql = """SELECT id, bar_name, bar_address 
             FROM locations 
             WHERE user_id = ?
             ORDER BY id DESC"""
    return db.query(sql, [user_id])
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import secrets
import config, location, users

app = Flask(__name__)
app.secret_key = config.secret_key

#homepage
@app.route("/")
def index():
    return render_template("index.html")

#location page
@app.route("/locations")
def locations():
    locations = location.get_locations()

    query = request.args.get("query")
    results = location.search(query) if query else []
    return render_template("locations.html", locations=locations, query=query, results=results)

# Uusi tietokohde, ja sen tulos
@app.route("/new_location")
def order():
    return render_template("order.html")


@app.route("/locations/<int:location_id>")
def show_location(location_id):
    thread = location.get_location(location_id)
    comments = location.get_comments(location_id)
    drinks = location.get_drinks(location_id)
    creator = location.get_creator(location_id)
    return render_template("locationpage.html", thread=thread, comments=comments, drinks=drinks, creator=creator)
    

@app.route("/new_comment", methods=["POST"])
def new_comment():
    check_csrf()
    content = request.form["content"]
    user_id = session["user_id"]
    location_id = request.form["location_id"]

    location.add_comment(content, user_id, location_id)
    return redirect("/locations/" + str(location_id))

@app.route("/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    comment = location.get_comment(comment_id)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", comment=comment)

    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        location.update_comment(comment["id"], content)
        return redirect("/locations/" + str(comment["location_id"]))
    
@app.route("/remove/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    comment = location.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", comment=comment)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            location.remove_comment(comment["id"])
        return redirect("/locations/" + str(comment["location_id"]))


@app.route("/editlocation/<int:location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    locationinfo = location.get_location(location_id)
    rows = location.get_drinks(location_id)

    drinks = {}
    for drink_id, drink_name, size, price in rows:
        if drink_name not in drinks:
            drinks[drink_name] = {}
        drinks[drink_name][size] = price

    return render_template("editlocation.html", locationinfo=locationinfo, drinks=drinks)


@app.route("/removelocation/<int:location_id>", methods=["GET", "POST"])
def remove_location(location_id):
    if "user_id" not in session:
        abort(403)

    locationinfo = location.get_location(location_id)

    if "user_id" not in session:
        abort(403)

    if request.method == "GET":
        return render_template("removelocation.html", locationinfo=locationinfo)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            location.remove_location(location_id)
        return redirect("/locations")



@app.route("/search")
def search():
    query = request.args.get("query")
    results = location.search(query) if query else []
    return render_template("locations.html", query=query, results=results)




@app.route("/result", methods=["POST"])
def result(): 
    check_csrf()
    try:
        if "user_id" not in session:
            return redirect("/login")

        location_id = request.form.get("location_id")

        bar_name = request.form.get("bar_name")
        bar_address= request.form.get("bar_address")
        extras = request.form.getlist("extra")
        extra_info = request.form.get("extra_info", "")


        if location_id:  
            location.update_location(
                location_id=location_id,
                bar_name=bar_name,
                bar_address=bar_address,
                happy_hour=1 if 'happy_hour' in extras else 0,
                student_discount=1 if 'student_discount' in extras else 0,
                gluten_free=1 if 'gluten_free' in extras else 0,
                student_patch=1 if 'student_patch' in extras else 0,
                extra_info=extra_info
            )
            current_location_id = location_id

        else:
            new_location_id = location.add_location(
                bar_name=bar_name,
                bar_address=bar_address,
                user_id=session["user_id"],
                happy_hour=1 if 'happy_hour' in extras else 0,
                student_discount=1 if 'student_discount' in extras else 0,
                gluten_free=1 if 'gluten_free' in extras else 0,
                student_patch=1 if 'student_patch' in extras else 0,
                extra_info=extra_info
            )
            current_location_id = new_location_id

        def check_price_add(location_id, drink_id, drink_size, price):
            if drink_size and price:
                location.add_price(location_id, drink_id, drink_size, price)

        # huge chunk of userinput from /order
        beer = request.form.get("beer")
        small_beer = request.form.get("small_beer")
        small_beer_price = request.form.get("small_beer_price")
        big_beer = request.form.get("big_beer")
        big_beer_price = request.form.get("big_beer_price")
        
        lonkero = request.form.get("lonkero")
        small_lonkero = request.form.get("small_lonkero")
        small_lonkero_price = request.form.get("small_lonkero_price")
        big_lonkero = request.form.get("big_lonkero")
        big_lonkero_price = request.form.get("big_lonkero_price")

        ananas = request.form.get("ananas")
        small_ananas = request.form.get("small_ananas")
        small_ananas_price = request.form.get("small_ananas_price")
        big_ananas = request.form.get("big_ananas")
        big_ananas_price = request.form.get("big_ananas_price")

        cider = request.form.get("cider")
        small_cider = request.form.get("small_cider")
        small_cider_price = request.form.get("small_cider_price")
        big_cider = request.form.get("big_cider")
        big_cider_price = request.form.get("big_cider_price")

        #create drinks (not a good way, later revision maybe)
        beer_id = location.add_drink(drink_name="beer")
        lonkero_id = location.add_drink(drink_name="lonkero")
        ananas_id = location.add_drink(drink_name="ananas")
        cider_id = location.add_drink(drink_name="cider")


        #add drinks to database (later revision..?)
        if beer:
            check_price_add(current_location_id, beer_id, small_beer, small_beer_price)
            check_price_add(current_location_id, beer_id, big_beer, big_beer_price)

        if lonkero:
            check_price_add(current_location_id, lonkero_id, small_lonkero, small_lonkero_price)
            check_price_add(current_location_id, lonkero_id, big_lonkero, big_lonkero_price)

        if ananas:
            check_price_add(current_location_id, ananas_id, small_ananas, small_ananas_price)
            check_price_add(current_location_id, ananas_id, big_ananas, big_ananas_price)

        if cider:
            check_price_add(current_location_id, cider_id, small_cider, small_cider_price)
            check_price_add(current_location_id, cider_id, big_cider, big_cider_price)



        return render_template(
            "result.html",
            bar_name=bar_name,
            bar_address=bar_address,
            extras=extras,
            extra_info=extra_info,
            beer=beer,
            small_beer=small_beer,
            small_beer_price=small_beer_price,
            big_beer=big_beer,
            big_beer_price=big_beer_price,
            lonkero=lonkero,
            small_lonkero = small_lonkero,
            small_lonkero_price=small_lonkero_price,
            big_lonkero=big_lonkero,
            big_lonkero_price=big_lonkero_price,
            ananas=ananas,
            small_ananas=small_ananas,
            small_ananas_price=small_ananas_price,
            big_ananas=big_ananas,
            big_ananas_price=big_ananas_price,
            cider=cider,
            small_cider=small_cider,
            small_cider_price=small_cider_price,
            big_cider=big_cider,
            big_cider_price=big_cider_price,
            current_location_id=current_location_id
            )
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred", 500
    

# login and registering

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return render_template("account_created.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    session["csrf_token"] = secrets.token_hex(16)
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"  
    result = db.query(sql, [username])

    
    
    if not result:
        return "VIRHE: väärä tunnus tai salasana"
        
    user_id, password_hash = result[0]
    
    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id  
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    session.clear()  
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    comments = users.get_comments(user_id)
    locations = users.get_locations(user_id)
    return render_template("user.html", user=user, comments=comments, locations=locations)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

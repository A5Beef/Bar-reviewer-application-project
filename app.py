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

# new location creation page
@app.route("/new_location")
def order():
    return render_template("order.html")

# locationpage
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

    if "user_id" not in session:
        return redirect("/login")


    content = request.form["content"].strip()
    user_id = session["user_id"]
    location_id = request.form["location_id"]

    if not content:
        return "VIRHE: kommentti ei voi olla tyhjä", 400


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

#search function
@app.route("/search")
def search():
    query = request.args.get("query")
    results = location.search(query) if query else []
    return render_template("locations.html", query=query, results=results)


#creation of new location and its result
@app.route("/result", methods=["POST"])
def result(): 
    check_csrf()
    try:
        if "user_id" not in session:
            return redirect("/login")

        # Get and check location info
        current_location_id, bar_name, bar_address, extras, extra_info = handle_location_form()

        # Get drink data
        drinks_data = get_drink_form_data()

        # Create drinks in db
        drink_ids = create_drinks_in_db()

        # add drinks to database
        add_drinks_prices(current_location_id, drink_ids, drinks_data)

        # Render result
        return render_template(
            "result.html",
            bar_name=bar_name,
            bar_address=bar_address,
            extras=extras,
            extra_info=extra_info,
            **drinks_data,
            current_location_id=current_location_id
        )
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Virhe: {str(e)}", 400


# helper functions

def handle_location_form():
    #Get location data and create/update location
    location_id = request.form.get("location_id")
    bar_name = request.form.get("bar_name", "").strip()
    bar_address = request.form.get("bar_address", "").strip()

    if not bar_name or not bar_address:
        raise ValueError("Nimi ja osoite ovat pakollisia kenttiä!")

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

    return current_location_id, bar_name, bar_address, extras, extra_info

# checks user input
def safe_price(price_str):
    try:
        price = float(price_str)
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price
    except (ValueError, TypeError):
        return None


def check_price_add(location_id, drink_id, drink_size, price):
    price_val = safe_price(price)
    if drink_size and price_val is not None:
        location.add_price(location_id, drink_id, drink_size, price_val)
    elif drink_size:
        raise ValueError(f"Invalid price for drink_id={drink_id}, size={drink_size}: {price}")

#     gets drinks from user
def get_drink_form_data():
    return {
        "beer": request.form.get("beer"),
        "small_beer": request.form.get("small_beer"),
        "small_beer_price": request.form.get("small_beer_price"),
        "big_beer": request.form.get("big_beer"),
        "big_beer_price": request.form.get("big_beer_price"),

        "lonkero": request.form.get("lonkero"),
        "small_lonkero": request.form.get("small_lonkero"),
        "small_lonkero_price": request.form.get("small_lonkero_price"),
        "big_lonkero": request.form.get("big_lonkero"),
        "big_lonkero_price": request.form.get("big_lonkero_price"),

        "ananas": request.form.get("ananas"),
        "small_ananas": request.form.get("small_ananas"),
        "small_ananas_price": request.form.get("small_ananas_price"),
        "big_ananas": request.form.get("big_ananas"),
        "big_ananas_price": request.form.get("big_ananas_price"),

        "cider": request.form.get("cider"),
        "small_cider": request.form.get("small_cider"),
        "small_cider_price": request.form.get("small_cider_price"),
        "big_cider": request.form.get("big_cider"),
        "big_cider_price": request.form.get("big_cider_price"),
    }

#    ensure all four drink types exist in DB and return their ids.
def create_drinks_in_db():
    return {
        "beer_id": location.add_drink("beer"),
        "lonkero_id": location.add_drink("lonkero"),
        "ananas_id": location.add_drink("ananas"),
        "cider_id": location.add_drink("cider"),
    }

#     Add all checked drinks and prices to the database
def add_drinks_prices(location_id, drink_ids, drinks_data):
    if drinks_data["beer"]:
        check_price_add(location_id, drink_ids["beer_id"], drinks_data["small_beer"], drinks_data["small_beer_price"])
        check_price_add(location_id, drink_ids["beer_id"], drinks_data["big_beer"], drinks_data["big_beer_price"])

    if drinks_data["lonkero"]:
        check_price_add(location_id, drink_ids["lonkero_id"], drinks_data["small_lonkero"], drinks_data["small_lonkero_price"])
        check_price_add(location_id, drink_ids["lonkero_id"], drinks_data["big_lonkero"], drinks_data["big_lonkero_price"])

    if drinks_data["ananas"]:
        check_price_add(location_id, drink_ids["ananas_id"], drinks_data["small_ananas"], drinks_data["small_ananas_price"])
        check_price_add(location_id, drink_ids["ananas_id"], drinks_data["big_ananas"], drinks_data["big_ananas_price"])

    if drinks_data["cider"]:
        check_price_add(location_id, drink_ids["cider_id"], drinks_data["small_cider"], drinks_data["small_cider_price"])
        check_price_add(location_id, drink_ids["cider_id"], drinks_data["big_cider"], drinks_data["big_cider_price"])



# login and registering
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")

    # Check for empty fields
    if not username or not password1 or not password2:
        return "VIRHE: täytä kaikki kentät", 400

    # Check if passwords match
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat", 400

    # Username validation
    if len(username) < 1:
        return "VIRHE: käyttäjätunnuksen on oltava vähintään 1 merkkiä pitkä", 400
    if " " in username:
        return "VIRHE: käyttäjätunnuksessa ei saa olla välilyöntejä", 400

    # Password validation
    if len(password1) < 1:
        return "VIRHE: salasanan on oltava vähintään 1 merkkiä pitkä", 400
    if " " in password1:
        return "VIRHE: salasanassa ei saa olla välilyöntejä", 400

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: käyttäjätunnus on jo varattu", 400

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

# csrf
def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

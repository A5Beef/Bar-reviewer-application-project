import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
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
        if "continue" in request.form:
            location.remove_comment(comment["id"])
        return redirect("/locations/" + str(comment["location_id"]))



    
@app.route("/editlocation/<int:location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    locationinfo = location.get_location(location_id)
    
    if request.method == "GET":
        return render_template("editlocation.html", locationinfo=locationinfo)

    if request.method == "POST":
        content = request.form["content"]
        location.update_location(location["id"], content)
        return redirect("/locations/" + str(locationinfo["location_id"]))


@app.route("/search")
def search():
    query = request.args.get("query")
    results = location.search(query) if query else []
    return render_template("locations.html", query=query, results=results)




@app.route("/result", methods=["POST"])
def result(): 
    try:
        if "user_id" not in session:
            return redirect("/login")

        bar_name = request.form.get("bar_name")
        bar_address= request.form.get("bar_address")
        extras = request.form.getlist("extra")
        extra_info = request.form.get("extra_info", "")

        

        new_location_id = location.add_location(bar_name=bar_name, bar_address=bar_address,
        user_id=session["user_id"],
        happy_hour=1 if 'happy_hour' in extras else 0,
        student_discount=1 if 'student_discount' in extras else 0,
        gluten_free=1 if 'gluten_free' in extras else 0,
        student_patch=1 if 'student_patch' in extras else 0,
        extra_info=extra_info )


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


        #add drinks to database (not a good way)
        if beer:
            location.add_price(location_id=new_location_id, drink_id=beer_id, drink_size=small_beer, price=small_beer_price)
            location.add_price(location_id=new_location_id, drink_id=beer_id, drink_size=big_beer, price=big_beer_price)

        if lonkero:
            location.add_price(location_id=new_location_id, drink_id=lonkero_id, drink_size=small_lonkero, price=small_lonkero_price)
            location.add_price(location_id=new_location_id, drink_id=lonkero_id, drink_size=big_lonkero, price=big_lonkero_price)

        if ananas:
            location.add_price(location_id=new_location_id, drink_id=ananas_id, drink_size=small_ananas, price=small_ananas_price)
            location.add_price(location_id=new_location_id, drink_id=ananas_id, drink_size=big_ananas, price=big_ananas_price)

        if cider:
            location.add_price(location_id=new_location_id, drink_id=cider_id, drink_size=small_cider, price=small_cider_price)
            location.add_price(location_id=new_location_id, drink_id=cider_id, drink_size=big_cider, price=big_cider_price)
            



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
            new_location_id=new_location_id
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

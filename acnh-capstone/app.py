from unicodedata import name
from webbrowser import get
from flask import Flask, render_template, request, jsonify, json, g, session, flash, redirect
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import User, Fish, UserFish, Fossil, UserFossil, UserBug, Bug, SeaCreature, UserSeaCreature, connect_db, db
import requests, random
from forms import RegisterForm, InputForm, LoginForm
from sqlalchemy import exc

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/acnh"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretpwdddd"

connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"

API_BASE_URL = f"https://acnhapi.com/v1"
ITEMS = ["fish", "sea", "bugs", "fossils"]

# ########################################################
def get_all_items_by_type(type):
    endpoint = f"{API_BASE_URL}/{type}"
    response = requests.get(endpoint)
    jresp = response.json()
    return jresp    

@app.before_request
def db_check():
    if Fish.query.first():
        return 
    for cats in ITEMS:
        resp = get_all_items_by_type(cats)
        if cats == "fish":
            for item in resp.keys():
                fish_data = Fish(name=resp[item]["name"]["name-USen"],
                    catch_phrase=resp[item]["catch-phrase"],
                    img_url=resp[item]["image_uri"])
                db.session.add(fish_data)
            db.session.commit()
        elif cats == "sea":
            for item in resp.keys():
                sea_data = SeaCreature(name=resp[item]["name"]["name-USen"],
                    catch_phrase=resp[item]["catch-phrase"],
                    img_url=resp[item]["image_uri"])
                db.session.add(sea_data)
            db.session.commit()
        elif cats == "fossils":
            for item in resp.keys():
                fossil_data = Fossil(name=resp[item]["name"]["name-USen"],
                    img_url=resp[item]["image_uri"])
                db.session.add(fossil_data)
            db.session.commit()
        elif cats == "bugs":
            for item in resp.keys():
                bug_data = Bug(name=resp[item]["name"]["name-USen"],
                    catch_phrase=resp[item]["catch-phrase"],
                    img_url=resp[item]["image_uri"])
                db.session.add(bug_data)
            db.session.commit()

###########################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
######################################

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup"""
    
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data)
            db.session.commit()

        except exc.IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)
        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logged out!", "success")
    
    return redirect("/login")

#########################################

@app.route("/", methods=["GET"])
def show_input_form():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/index")

    cats = {"empty" : "",
            "fish":"Fish",
            "sea_creature": "Sea Creature", 
            "fossil": "Fossil", 
            "bug": "Bug"}

    fish = Fish.query.all()
    sea_creature = SeaCreature.query.all()
    fossil = Fossil.query.all()
    bug = Bug.query.all()
    user = User.query.get_or_404(g.user.id)

    return render_template("users/input_form.html", user=user, cats=cats, fish=fish, sea_creature=sea_creature, fossil=fossil, bug=bug)

@app.route("/index")
def homepage():
    """Homepage w/urls to items"""
    
    return render_template("home.html")

##############################
@app.route("/users/<int:user_id>/items", methods=["GET", "POST"])
def list_users_items(user_id):
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/index")

    user = User.query.get_or_404(user_id)

    users_fish = (
        Fish.query.join(User, Fish.users).filter(User.id==user_id).all()
    )
    users_bug = (
        Bug.query.join(User, Bug.users).filter(User.id==user_id).all()
    )
    users_seacreature = (
        SeaCreature.query.join(User, SeaCreature.users).filter(User.id==user_id).all()
    )
    users_fossil = (
        Fossil.query.join(User, Fossil.users).filter(User.id==user_id).all()
    )

    if request.form.get('cat_name', None) is not None:
        if request.form['cat_name'] == "fish":
            db_fish = Fish.query.filter(Fish.name==request.form["fish_name"]).one()

            new_fish = UserFish(user_id=user.id, fish_id=db_fish.id)
            db.session.add(new_fish)
            db.session.commit()

        if request.form['cat_name'] == "fossil":
            db_fossil = Fossil.query.filter(Fossil.name==request.form["fossil_name"]).one()

            new_fossil = UserFossil(user_id=user.id, fossil_id=db_fossil.id)
            db.session.add(new_fossil)
            db.session.commit()

        if request.form['cat_name'] == "bug":
            db_bug = Bug.query.filter(Bug.name==request.form["bug_name"]).one()

            new_bug = UserBug(user_id=user.id, bug_id=db_bug.id)
            db.session.add(new_bug)
            db.session.commit()

        if request.form['cat_name'] == "sea_creature":
            db_seacreature = SeaCreature.query.filter(SeaCreature.name==request.form["sea_creature_name"]).one()

            new_seacreature = UserSeaCreature(user_id=user.id, screature_id=db_seacreature.id)
            db.session.add(new_seacreature)
            db.session.commit()

        users_fish = (
        Fish.query.join(User, Fish.users).filter(User.id==user_id).all()
        )
        users_bug = (
        Bug.query.join(User, Bug.users).filter(User.id==user_id).all()
        )
        users_seacreature = (
        SeaCreature.query.join(User, SeaCreature.users).filter(User.id==user_id).all()
        )
        users_fossil = (
        Fossil.query.join(User, Fossil.users).filter(User.id==user_id).all()
        )

    
    return render_template("users/items.html", user=user, users_fish=users_fish, users_bug=users_bug, users_fossil=users_fossil, users_seacreature=users_seacreature)

#################################
@app.route("/fishes")
def get_fishes_list():
    """Show all fishes"""

    fishes = Fish.query.all()

    return render_template("cats/fishes.html", fishes=fishes)

@app.route("/fossils")
def get_fossils_list():
    """Show all fossils"""

    fossils = Fossil.query.all()

    return render_template("cats/fossils.html", fossils=fossils)

@app.route("/bugs")
def get_bugs_list():
    """Show all bugs"""

    bugs = Bug.query.all()

    return render_template("cats/bugs.html", bugs=bugs)
    
@app.route("/sea_creatures")
def get_screatures_list():
    """Show all sea creatures"""

    sea_creatures = SeaCreature.query.all()

    return render_template("cats/sea_creatures.html", sea_creatures=sea_creatures)
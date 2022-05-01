"""Model for Animal Crossing New Horizons Museum Catalog app"""

from click import password_option
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()
DEFAULT_URL = "https://img.game8.co/3279200/c0865f56986ecfb1d98f1abd53d91615.png/show"


# def image_url(self):
#     """Return image or confused reaction"""
#     return self.img_url or DEFAULT_URL

class User(db.Model):
    """Users"""

    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    fishes = db.relationship("Fish", secondary="users_fish", backref="users")
    bugs = db.relationship("Bug", secondary="users_bug", backref="users")
    sea_creatures = db.relationship("SeaCreature", secondary="users_seacreature", backref="users")
    fossils = db.relationship("Fossil", secondary="users_fossil", backref="users")

    @classmethod
    def register(cls, username, password):
        """Register user w/hashed pw & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = User(
            username=username,
            password=hashed_utf8)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate user exists & pw correct. 
        Return user if valid, return false otherwise"""

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class Fish(db.Model):
    """Fish"""

    __tablename__= "fishes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    catch_phrase = db.Column(db.String)
    img_url = db.Column(db.String, default=DEFAULT_URL)

class UserFish(db.Model):
    """Users fish collection"""

    __tablename__= "users_fish"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    fish_id = db.Column(db.Integer, db.ForeignKey("fishes.id"), primary_key=True)


class Fossil(db.Model):
    """Fossil"""

    __tablename__= "fossils"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    img_url = db.Column(db.String, default=DEFAULT_URL)

class UserFossil(db.Model):
    """Users fossil collection"""

    __tablename__= "users_fossil"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    fossil_id = db.Column(db.Integer, db.ForeignKey("fossils.id"), primary_key=True)

class SeaCreature(db.Model):
    """Sea Creatures"""

    __tablename__= "sea_creatures"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    catch_phrase = db.Column(db.String)
    img_url = db.Column(db.String, default=DEFAULT_URL)

class UserSeaCreature(db.Model):
    """Users sea creature collection"""

    __tablename__= "users_seacreature"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    screature_id = db.Column(db.Integer, db.ForeignKey("sea_creatures.id"), primary_key=True)

class Bug(db.Model):
    """Bug"""

    __tablename__= "bugs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    catch_phrase = db.Column(db.String)
    img_url = db.Column(db.String, default=DEFAULT_URL)

class UserBug(db.Model):
    """Users bug collection"""

    __tablename__= "users_bug"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    bug_id = db.Column(db.Integer, db.ForeignKey("bugs.id"), primary_key=True)

def connect_db(app):

    db.app = app
    db.init_app(app)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """User registration form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=50)])

class LoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class InputForm(FlaskForm):
    """Feedback form"""
    
    item = StringField("Item type")
    item_name = StringField("Item name")
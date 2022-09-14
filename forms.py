from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	passw = PasswordField("Password", validators = [DataRequired()])
	confirm_passw = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
	comp = StringField("Company Name", validators = [DataRequired()])
	rep_name = StringField("Representative Name", validators = [DataRequired()])
	rep_lname = StringField("Representative Last Name", validators = [DataRequired()])
	rep_pnum = StringField("Representative Phone Number", validators = [DataRequired()])
	submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	passw = PasswordField("Password", validators = [DataRequired()])
	rem = BooleanField("Remember Me")
	submit = SubmitField("Log In")
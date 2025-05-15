# app/forms.py
import calendar
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import IntegerField, SelectField, FileField, URLField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, URL, Optional
from flask_wtf.file import FileAllowed

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
class CompetitionForm(FlaskForm):
    name = StringField("Competition Name", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    month = SelectField("Month", choices=[('', '– Select Month –')] + [(str(i), calendar.month_name[i]) for i in range(1, 13)], validators=[DataRequired()])
    day = IntegerField("Day", validators=[DataRequired(), NumberRange(min=1, max=31)])

    poster_file = FileField("Upload Poster", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    poster_link = URLField("Poster URL", validators=[Optional(), URL()])

    logo_file = FileField("Upload Logo", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    logo_link = URLField("Logo URL", validators=[Optional(), URL()])

    comp_link = URLField("Competition Link", validators=[DataRequired(), URL()])

    action = HiddenField()  # “public”、“private”或“share”，由 JS 设置
    bracket_data = HiddenField()
    submit = SubmitField("Submit")

class PlayerForm(FlaskForm):
    player_name = StringField("Name", validators=[DataRequired()])
    league = StringField("League", validators=[DataRequired()])

    photo_file = FileField("Upload Image", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    photo_link = URLField("Image URL", validators=[Optional(), URL()])

    twitter_link = URLField("Twitter Link", validators=[Optional(), URL()])
    twitch_link = URLField("Twitch Link", validators=[Optional(), URL()])

    action = HiddenField()  # “public” or “private”
    submit = SubmitField("Submit")

class DeleteCompetitionForm(FlaskForm):
    comp_id = HiddenField("Competition ID")
    submit = SubmitField("Delete")

class ShareCompetitionForm(FlaskForm):
    comp_id = HiddenField("Competition ID")
    share_with = StringField("Share With", validators=[DataRequired()])
    submit = SubmitField("Send Share")

class DeletePlayerForm(FlaskForm):
    player_id = HiddenField()
    submit = SubmitField("Delete")
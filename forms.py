from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length

# class RegisterForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
#     name = StringField("Name", validators=[DataRequired()])
#     submit = SubmitField("Sign ME Up!")

# class LoginForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Sign ME In!")

class AdminForm(FlaskForm):
    article = StringField("Article", validators=[DataRequired()])
    publish_date = PasswordField("Publish At", validators=[DataRequired()])
    submit = SubmitField("Submit!")
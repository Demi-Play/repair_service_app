from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OrderForm(FlaskForm):
    service_id = SelectField('Service', coerce=int)  # Заполнить данными из базы
    submit = SubmitField('Order Service')

class PortfolioForm(FlaskForm):
    image_url = StringField('Image URL', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add to Portfolio')
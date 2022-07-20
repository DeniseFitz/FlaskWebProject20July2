"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
 
from FlaskWebProject20July2 import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import pandas as pd

app.config['SECRET_KEY'] = 'fb93246348ed383a9de5b7e77ff8d579' # be sure to use only the most recent key generated
#name of the database to create or use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'

db = SQLAlchemy(app)

#Because of __tablename__ database table is 'usertable"
class User(db.Model):
  __tablename__ = 'usertable' #if do not specify the table name is user
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"usertable('{self.username}', '{self.email}', '{self.password}')"


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST' and form.validate():
            user_a = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user_a)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', year=datetime.now().year,
        message='Your register description page.',form=form)

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[Length(min=6, max=35)])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
                                     
    submit = SubmitField('Sign Up')   


#new code added to make sure usertable is created
db.create_all()
 


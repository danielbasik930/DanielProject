"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DanielProject import app
from DanielProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from DanielProject.Models.QueryFormStructure import QueryFormStructure 
from DanielProject.Models.QueryFormStructure import LoginFormStructure 
from DanielProject.Models.QueryFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 
SECRET_KEY = 'my super secret key'.encode('utf8')


@app.route('/Home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='',
        year=datetime.now().year,
        
    )


@app.route('/Album')
def Album():
    """Renders the about page."""
    return render_template(
        'PictureAlbum.html',
        title='Pictures',
        year=datetime.now().year,
        message='Welcome to my picture album'
    )


@app.route('/Query', methods=['GET', 'POST'])
def Query():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\toprun.csv'))
    


    form = QueryFormStructure(request.form)
    form.event.choices =[('100 m','100 m'),('200 m','200 m'),('400 m','400 m'),('800 m','800 m'),('1500 m','1500 m'),('5000 m','5000 m'),('10000 m','10000 m'),('Half marathon','Half marathon') ,('Marathon','Marathon')]
    form.gender.choices =[('Men','Men'),('Women','Women')]
    chart =''
    
    if request.method=='POST':
        ev = form.event.data
        gn = form.gender.data
        columns = ['Name','City','Place','Date of Birth','Date','Time']
        df.drop(columns, inplace=True, axis=1)
        df=df[df['Event']== ev]
        df=df[df['Gender']== gn]
        g = df.groupby('Country').size()
        g = g.sort_values(ascending= False)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        g.plot(kind='bar', ax = ax)
        chart = plot_to_img(fig)

    return render_template('Query.html', 
            form = form,
            chart = chart,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('Query')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )





@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou top runnig ',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to work on   '
    )




from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from DanielProject.Models.Forms import ExpandForm
from DanielProject.Models.Forms import CollapseForm

@app.route('/data/toprun' , methods = ['GET' , 'POST'])
def DataSet1():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\toprun.csv'))
    raw_data_table = ''
    
    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    return render_template(
        'DataSet1.html',
        title='The Run Results records',
        year=datetime.now().year ,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )
@app.route('/data/citiy_csv_short_from_oran' , methods = ['GET' , 'POST'])
def DataSet():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\citiy_csv_short_from_oran.csv'))
    raw_data_table = ''
    
    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    return render_template(
        'DataSet.html',
        title='All the heights of the world',
        year=datetime.now().year ,
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String




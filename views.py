"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from Interface import app
from Interface import DataAnalyzer
import matplotlib.pyplot as plt

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    projects = []
    return render_template(
        'index.html',
        title='My Projects',
        projects = projects
    )

@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def homepost():
    projects = []
    return render_template(
        'index.html',
        title='My Projects',
        projects = projects
    )

@app.route('/createproject')
def createproject():
    return render_template(
        'createproject.html',
        title='Create New Project'
    )

@app.route('/datainsight/<id>')
def datainsight(id):
   type = request.args.get('type')
   columns = ['order_id','user_id','eval_set','order_number','order_dow','order_hour_of_day','days_since_prior_order','add_to_cart_order','reordered','product_id']
   basicInfo = {}
   if type == "basic":
       basicInfo = DataAnalyzer.basicInfo(id)
   elif type=='stats':
       DataAnalyzer.dataStats(id)
   elif type=='attrcor':
       DataAnalyzer.dataAttrCorrelation(id);
   elif type=='unidist':
       DataAnalyzer.univariantDist(id);

   return render_template(
        'datainsight.html',
        title='Data Insight',
        id = id,
        type=type,
        basicInfo = basicInfo
    )

@app.route('/createproject', methods=['POST'])
def hello():
    name=request.form['name']
    email=request.form['description']
    return render_template('editproject.html', name=name, email=email)

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

@app.route('/datainsight/head/<id>')
def datainsighthead(id):
    page = "../../projects/{}/head.html".format(id)
    return render_template(
        page
    )

@app.route('/services', methods=['GET'])
def services():
    services = []
    result = [];
    for s in services:
        rec = {"name": s[1], "description": s[2], "project" : s[6], "servicename": s[5]}

    return render_template(
        'services.html',
        title='My Services',
        services = result
    )
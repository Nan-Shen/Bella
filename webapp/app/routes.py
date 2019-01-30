from flask import render_template, flash, redirect, Flask, jsonify, request
from app import app
from .forms import IndexForm, CustomerForm, BusinessForm
from .search import BellaSearch

import os
import pandas as pd

#app = Flask(__name__)

# login view function suppressed for brevity

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if form.validate_on_submit():
       if form.identity.data == 'customer':
            return redirect('/customer')
       else:
            return redirect('/business')
    return render_template('index.html',
                           title='Home',
                           form=form)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'test on'

@app.route('/business', methods=['GET', 'POST'])
def business():
    form = BusinessForm()
    if form.validate_on_submit():
        flash('Analysing customer preference for %s ...' % form.category.data)
        return redirect('/index')
    return render_template('business.html', 
                           title='Bella business',
                           form=form)
    
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = CustomerForm()
    products = []
    if form.validate_on_submit():
        concerns = form.concerns.data
        category = form.category.data
        flash('Searching for %s best for/ that\'s %s ...' % 
              (concerns, category))
        bs = BellaSearch()
        products = bs.CustomizedSearch(concerns, category)
    return render_template('customer.html',
                           title='Bella customer',
                           form=form,
                           products=products)
 
"""
#@app.route('/search', methods=['GET', 'POST'])
#def search_products():
        query_json = request.get_json()
        query = pd.read_json(query_json, orient='records')
        category = str(query['category'].values)
        concerns = str(query['concerns'].values)
        #To resolve the issue of TypeError: Cannot compare types 
        #'ndarray(dtype=int64)' and 'str'
"""
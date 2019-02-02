from flask import render_template, flash, redirect, Flask, jsonify, request, Response, make_response
from app import app
from .forms import IndexForm, CustomerForm, BusinessForm
from .search import BellaSearch
from .predict import BellaModel

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

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
    rating = []
    plot_url = []
    if form.validate_on_submit():
        flash('Analysing customer preference for %s ...' % form.category.data)
        bm = BellaModel()
        rating = [{'rate':bm.PredictRating(form.category.data,
                                           form.review.data)}]
        plot_url = ["data:image/png;base64,%s" % bm.PlotFeatureImportance()]
    return render_template('business.html', 
                           title='Bella business',
                           form=form,
                           rating=rating,
                           plot_url=plot_url)
    
@app.route('/plot.png')
def plot_png():
    bs = BellaSearch()
    fig = bs.PlotFeatureImportance()
    response = make_response(fig)
    response.mimetype = 'image/png'
    return response
    
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = CustomerForm()
    products = []
    if form.validate_on_submit():
        concerns = form.concerns.data
        category = form.category.data
        flash('Searching for %s best for/ that\'s %s ...' % 
              (category, concerns))
        bs = BellaSearch()
        products = bs.CustomizedSearch(concerns, category)
    return render_template('customer.html',
                           title='Bella customer',
                           form=form,
                           products=products)

    
    
from flask import render_template, flash, redirect, make_response, send_from_directory
from app import app
from .forms import IndexForm, CustomerForm, BusinessForm
from .search import BellaSearch
from .predict import BellaModel

#app = Flask(__name__)


# login view function suppressed for brevity

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html',
                           title='Home',
                           customer_url='/customer',
                           business_url='/business',
                           me_url='/me')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

@app.route('/business', methods=['GET', 'POST'])
def business():
    form = BusinessForm()
    reviews = []
    plot_url = []
    if form.validate_on_submit():
        bm = BellaModel()
        reviews, url = bm.topic_summary(form.topic.data, 
                                        form.category.data, 
                                        random=form.random.data, 
                                        n=2)
        
        plot_url = ["data:image/png;base64,%s" % url]
        
    return render_template('business.html', 
                           title='Business Analyst',
                           form=form,
                           reviews=reviews,
                           plot_url=plot_url)

@app.route('/plot.png')
def plot_png():
    bs = BellaSearch()
    fig = bs.PlotFeatureImportance()
    response = make_response(fig)
    response.mimetype= 'image/png'
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
                           title='Beauty Advisor',
                           form=form,
                           products=products)

@app.route('/me', methods=['GET', 'POST'])
def me():
    
    return render_template('me.html',
                           title='Me')
    
    
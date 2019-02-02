from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired

topics = ['aging', 'unclear', 'make up', 'look + scent', 'acne', 'pore + sensitive', 'price', 'routine']
CHOICES = [(n, t) for t,n in zip(topics, range(8))]

class IndexForm(FlaskForm):
    identity = SelectField('user_identity', 
                          choices=[('customer', 'Customer'), 
                                   ('business', 'Business')],
                          default='Customer')
    #openid = StringField('openid', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)
    
class CustomerForm(FlaskForm):
    concerns = StringField('skin_concerns', validators=[DataRequired()])
    category = SelectField('product_types', 
                          choices=[('toner', 'Toner'), 
                                   ('moisterizer', 'Moisterizer'), 
                                   ('Face Serums', 'Serum')],
                          default='Serum')
class BusinessForm(FlaskForm):
    category = SelectField('customer_group', 
                           choices=[('c_skintype', 'Skin Type'), 
                                   ('c_skinconcerns', 'Skin Concerns'), 
                                   ('c_age', 'Age')],
                           validators=[DataRequired()])
    random = BooleanField('Random Reviews')
    topic = SelectField('customer_group', choices=[('0', 'aging'),
                                                   ('1', 'unclear'),
                                                    ('2', 'make up'),
                                                    ('3', 'look + scent'),
                                                    ('4', 'acne'),
                                                    ('5', 'pore + sensitive'),
                                                    ('6', 'price'),
                                                    ('7', 'routine')])

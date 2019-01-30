from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

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
    category = SelectField('product_types', 
                          choices=[('toner', 'Toner'), 
                                   ('moisterizer', 'Moisterizer'), 
                                   ('serum', 'Serum')],
                          default='Serum',
                          validators=[DataRequired()])

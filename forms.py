from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, URLField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image_url = URLField('Image URL (Optional)')
    submit = SubmitField('Add Book')

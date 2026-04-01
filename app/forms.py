from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError
from decimal import Decimal

class PropertyForm(FlaskForm):
    # Text fields with validation
    title = StringField('Property Title', validators=[
        DataRequired(message='Title is required'),
    ])
    
    bedrooms = IntegerField('No. Bedrooms', validators=[
        DataRequired(message='Number of bedrooms is required')
    ])
    
    bathrooms = IntegerField('No. Bathrooms', validators=[
        DataRequired(message='Number of bathrooms is required'),
    ])
    
    location = StringField('Location', validators=[
        DataRequired(message='Location is required')
    ])
    
    price = DecimalField('Price', validators=[
        DataRequired(message='Price is required'),
    ], places=2)
    
    # Select field for property type
    property_type = SelectField('Property Type', choices=[
        ('house', 'House'),
        ('apartment', 'Apartment')
    ], validators=[DataRequired(message='Please select a property type')])
    
    # Textarea field for description
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
    ])
    
    # File upload field
    photo = FileField('Photo', validators=[
        FileRequired(message='Please select a photo'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only! (jpg, jpeg, png, gif)')
    ])
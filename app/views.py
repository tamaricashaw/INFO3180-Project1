"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
import uuid

from app import app
from flask import flash, render_template, request, redirect, url_for, send_from_directory

from app.forms import PropertyForm
from .models import Property, db 


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")






ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename):
    """Generate a unique filename to avoid collisions"""
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()
    upload_folder = app.config['UPLOAD_FOLDER']

    if form.validate_on_submit():
        # Handle file upload
        photo_file = form.photo.data
        
        if photo_file and allowed_file(photo_file.filename):
            # Generate unique filename
            filename = generate_filename(photo_file.filename)
            
            # Ensure upload directory exists
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(upload_folder, filename)
            photo_file.save(file_path)
            
            # Create new property instance
            new_property = Property(
                title=form.title.data,
                description=form.description.data,
                bedroom=form.bedrooms.data,
                bathroom=form.bathrooms.data,
                location=form.location.data,
                price=form.price.data,
                property_type=form.property_type.data,
                photo_filename=filename
            )
            
            # Save to database
            db.session.add(new_property)
            db.session.commit()
            
            flash('Property successfully added!', 'success')
            return redirect(url_for('properties'))
        else:
            flash('Invalid file type. Please upload an image (jpg, jpeg, png, gif)', 'danger')
    
    return render_template('add_property.html', form=form)


# Route 2: Display list of all properties
@app.route('/properties')
def properties():
    # Query all properties from database, ordered by id descending (newest first)
    properties_list = Property.query.order_by(Property.id.desc()).all()
    return render_template('properties_list.html', properties=properties_list)


# Route 3: Display individual property by ID
@app.route('/properties/<int:propertyid>')
def property_detail(propertyid):
    # Query property by ID
    property = Property.query.get_or_404(propertyid)
    return render_template('property_detail.html', property=property)


# Route to serve uploaded images
@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    """Serve uploaded files from the app/uploads folder"""
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)





###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
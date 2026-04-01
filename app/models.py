from . import db



class Property(db.Model):
  
    __tablename__ = 'Properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    bedroom = db.Column(db.Integer)
    bathroom = db.Column(db.Integer)
    location = db.Column(db.String(128))
    price = db.Column(db.Numeric(10, 2))
    property_type = db.Column(db.String(80))
    photo_filename = db.Column(db.String(128))



    def __init__(self, title,description,bedroom,bathroom,location,price,property_type,photo_filename):
        self.title = title
        self.description = description
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.location = location
        self.price = price
        self.property_type = property_type
        self.photo_filename = photo_filename


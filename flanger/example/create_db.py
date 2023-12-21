from models import *
from app import *

with app.app_context():
    db.create_all()

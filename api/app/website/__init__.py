from flask import Blueprint
website_bp = Blueprint('website_bp', __name__)
from app.website import routes
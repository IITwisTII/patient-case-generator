from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
    app.secret_key = 'BAD_SECRET_KEY'
    CORS(app)  # Enable CORS for all routes
    
    from .api_routes import api_routes
    app.register_blueprint(api_routes)
    
    return app

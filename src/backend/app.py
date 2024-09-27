from flask import Flask
from flask_cors import CORS
from api_routes import api_routes

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app)  # Enable CORS for all routes
    
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)

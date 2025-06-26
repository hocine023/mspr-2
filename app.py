import os
import sys
import pandas as pd
import plotly.express as px
from flask import Flask
from flask_cors import CORS 
from flasgger import Swagger
from dotenv import load_dotenv

# === Routes internes ===
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp
from routes.prediction import bp as prediction_bp

# === Paths supplémentaires ===
sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

# === Configuration upload ===
UPLOAD_FOLDER = 'donnes'
CLEAN_DATA_FOLDER = '../donnes_clean/'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    load_dotenv()
    app = Flask(__name__) 
    CORS(app)

    # === Config & JWT ===
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # ✅ Configuration Swagger
    app.config['SWAGGER'] = {
        'title': 'Pandemic API',
        'uiversion': 3
    }

    Swagger(app)

    # === Enregistrement des blueprints ===
    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(daily_pandemic_country_bp)
    @app.route("/")
    def home():
        return "API is running"

    return app
   
def main():
    app = create_app()
    app.run(debug=True, host="0.0.0.0")  # ✅ Important pour Docker

if __name__ == "__main__":
    main()

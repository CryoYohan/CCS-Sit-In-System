from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def create_app():
    """Application factory function."""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Load configuration (optional)
    app.config.from_pyfile('config.py', silent=True)

    # # Define the directory where images will be stored
    # UPLOAD_FOLDER = 'static/uploads'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Import and register blueprints (routes)
    from .routes import main  # Import your routes
    from .adminroute import admin # Register admin route
    from .staffroute import staff

    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(staff)

    return app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if config_class:
        app.config.from_object(config_class)
    else:
        # Load configuration from a config file if it exists
        app.config.from_mapping(
            SECRET_KEY='dev',  # Change this for production
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # The name of the login view

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user_id))

    with app.app_context():
        # Import parts of our application
        from . import models
        from .routes import bp
        app.register_blueprint(bp)

        # Create database tables for our models
        db.create_all()

        return app

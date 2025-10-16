from flask import Flask

from views.auth import bp as auth_bp
from views.users import bp as users_bp


def create_blueprints(app: Flask):
    """Register all blueprints with the Flask application."""

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

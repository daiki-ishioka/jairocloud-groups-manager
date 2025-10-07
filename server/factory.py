from flask import Flask

from ext import MapWebUI


def create_app(config_object="config.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    _map_web_ui = MapWebUI(app)

    @app.route("/")
    def home():
        return "Welcome to the mAP Web UI!"

    return app

from flask import Flask
from app.routes import home, dashboard

def create_app(test_config=None):
    # set up app config to serve static from root
    app = Flask(__name__, static_url_path='/')
    # make trailing slashes optional
    app.url_map.strict_slashes = False
    # session key
    app.config.from_mapping(SECRET_KEY='SECRETKEY_123')

    # define routes
    @app.route('/hello')
    def hello():
        return 'hello world'

    # register the routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)

    return app

from flask import Flask
from app.routes import home, dashboard, api
from app.db import init_db
from app.utils import filters

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
    app.register_blueprint(api)

    # connect to the db instance using app instance so we can track connection in context
    init_db(app)

    app.jinja_env.filters['format_url'] = filters.format_url
    app.jinja_env.filters['format_date'] = filters.format_date
    app.jinja_env.filters['format_plural'] = filters.format_plural

    return app

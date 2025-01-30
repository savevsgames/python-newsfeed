from flask import Flask


def create_app(test_config=None):
    # set up app config to serve static from root
    app = Flask(__name__, static_url_path='/')
    # make trailing slashes optional
    app.url_map.strict_slashes = False
    # session key
    app.config.from_mapping(SECRET_KEY='SECRETKEY_123')

    return app

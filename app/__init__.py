from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_dance.contrib.google import make_google_blueprint
import os

db = SQLAlchemy()

def create_app(config_class=Config):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #TODO: remove this line before deploying
    app = Flask(__name__)
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SERVER_NAME'] = 'self-count9.iwataku.site'
    app.config.from_object(Config)
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=True,
    )

    db.init_app(app)

    google_bp = make_google_blueprint(
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        offline=True,
        scope=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ],
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    from app import routes, auth
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)

    return app

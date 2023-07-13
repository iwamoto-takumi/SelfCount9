from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import google

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get("/oauth2/v1/userinfo")
    session['google_token'] = resp.json()
    return redirect(url_for('routes.home'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.home'))

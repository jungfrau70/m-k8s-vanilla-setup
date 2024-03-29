import json

import flask
from flask import Flask, render_template, g, redirect
import flask_login
from flask_login import login_required
from flask_oidc import OpenIDConnect

from model.user import User

import urllib

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'foo@bar.com': {'pw': 'secret'}}

app.config.update({
    'SECRET_KEY': 'be91aef3-1540-4e27-b2dd-5f87ce5752f7',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
#    'OIDC_VALID_ISSUERS': ['http://keycloak.alphatics.com/auth/realms/hms'],
#    'OIDC_OPENID_REALM': 'http://183.111.230.171:5001/oidc_callback'
})
oidc = OpenIDConnect(app)


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['email', 'openid_id'])
    return ('Hello, %s (%s)! <a href="/">Return</a>' %
            (info.get('email'), info.get('openid_id')))


@app.route('/api')
@oidc.require_login
#accept_token(require_token=True)
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % str(g) + str(oidc)})


@app.route('/logout')
def logout():
    oidc.logout()
    redirect_uri = urllib.quote_plus('http://183.111.230.171:5001')
    return redirect('http://keycloak.alphatics.com/auth/realms/hms/protocol/openid-connect/logout?redirect_uri=%s' % redirect_uri)
#    return 'Hi, you have been logged out! <a href="/">Return</a>'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)

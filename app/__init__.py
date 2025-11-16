import os
from flask import Flask
from okta import UsersClient
from flask_bcrypt import Bcrypt
from flask_oidc import OpenIDConnect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Configuration
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable is required. Please set it in your .env file.")
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///site.database')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OIDC Configuration
app.config["OIDC_CLIENT_SECRETS"] = os.environ.get("OIDC_CLIENT_SECRETS", "client_secrets.json")
app.config["OIDC_COOKIE_SECURE"] = os.environ.get("OIDC_COOKIE_SECURE", "False").lower() == "true"
app.config["OIDC_CALLBACK_ROUTE"] = os.environ.get("OIDC_CALLBACK_ROUTE", "/oidc/callback")
app.config["OIDC_SCOPES"] = os.environ.get("OIDC_SCOPES", "openid email profile").split()
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = os.environ.get("OIDC_ID_TOKEN_COOKIE_NAME", "oidc_token")
app.config["OIDC_ID_TOKEN_COOKIE_SECURE"] = os.environ.get("OIDC_ID_TOKEN_COOKIE_SECURE", "False").lower() == "true"

# Okta Configuration
okta_url = os.environ.get("OKTA_URL", "https://dev-770962.okta.com")
okta_api_token = os.environ.get("OKTA_API_TOKEN", "")

if not okta_api_token:
    raise ValueError("OKTA_API_TOKEN environment variable is required")

oidc = OpenIDConnect(app)
okta_client = UsersClient(okta_url, okta_api_token)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

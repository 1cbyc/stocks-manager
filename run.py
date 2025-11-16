import os
from app import app, db
from app.routes.routes import stocks_blueprint


app.register_blueprint(stocks_blueprint, url_prefix='/stocks')

# Initialize database tables (only creates tables that don't exist)
with app.app_context():
    db.create_all()

production = os.environ.get("PRODUCTION", "False").lower() == "true"


if __name__ == '__main__':
    if production:
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(host='127.0.0.1', port=8001, debug=True)


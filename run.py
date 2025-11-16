import os
from app import app
from app.routes.routes import stocks_blueprint


app.register_blueprint(stocks_blueprint, url_prefix='/stocks')

production = os.environ.get("PRODUCTION", "False").lower() == "true"


if __name__ == '__main__':
    if production:
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(host='127.0.0.1', port=8001, debug=True)


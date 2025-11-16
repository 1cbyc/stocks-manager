from app.models.stock import Stock, StockError
from app.forms.forms import AddStockForm
from app.database.database import StockDb
from app import db, oidc, app, okta_client
from flask import Blueprint, render_template, request, redirect, url_for, flash, g

stocks_blueprint = Blueprint('stocks', __name__)


@app.before_request
def before_request():
    """Set up user context before each request."""
    try:
        if oidc.user_loggedin:
            user_sub = oidc.user_getfield("sub")
            if user_sub:
                g.user = okta_client.get_user(user_sub)
            else:
                g.user = None
        else:
            g.user = None
    except Exception as e:
        # Log error but don't break the request
        # In production, you'd want to log this properly
        g.user = None


@stocks_blueprint.route('/main', methods=['GET', 'POST'])
@oidc.require_login
def main():
    # Get current user ID from Okta
    user_id = oidc.user_getfield("sub") if oidc.user_loggedin else None
    
    if not user_id:
        flash('Please log in to view your portfolio', 'alert-danger')
        return redirect(url_for('stocks.login'))
    
    # Filter stocks by user_id
    stocks = StockDb.query.filter_by(user_id=user_id).all()
    total = Stock.get_total(stocks)
    form = AddStockForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            stock_symbol = request.form['stock_symbol']
            num_of_shares = request.form['num_of_shares']
            purchase_price = request.form['purchase_price']

            # Validate input values
            num_of_shares = float(num_of_shares)
            purchase_price = float(purchase_price)
            
            if num_of_shares <= 0:
                flash('Number of shares must be greater than 0', 'alert-danger')
                return redirect(url_for('stocks.main'))
            
            if purchase_price <= 0:
                flash('Purchase price must be greater than 0', 'alert-danger')
                return redirect(url_for('stocks.main'))

            try:
                stock = Stock(stock_symbol, num_of_shares, purchase_price)
                info = stock.stock_data
            except StockError as e:
                flash(str(e), 'alert-danger')
                return redirect(url_for('stocks.main'))

            # Check if stock already exists for this user
            existing_stock = StockDb.query.filter_by(
                user_id=user_id,
                stock_symbol=info['stock_symbol']
            ).first()
            
            if existing_stock:
                flash(f'{stock_symbol.upper()} is already in your portfolio', 'alert-warning')
                return redirect(url_for('stocks.main'))

            stock_db = StockDb(
                id=info['_id'],
                user_id=user_id,
                full_name=info['full_name'],
                stock_symbol=info['stock_symbol'],
                shares=info['shares'],
                purchase_price=info['purchase_price'],
                net_buy_price=info['net_buy_price'],
                logo=info['logo'] or ''
            )

            db.session.add(stock_db)
            db.session.commit()

            flash(f'{stock_symbol.upper()} stock was added successfully', 'alert-success')
            return redirect(url_for('stocks.main'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'alert-danger')
            return redirect(url_for('stocks.main'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding stock: {str(e)}', 'alert-danger')
            return redirect(url_for('stocks.main'))

    return render_template('stocks/table.html', stocks=stocks, Stock=Stock, total=total, form=form)


@stocks_blueprint.route('/login', methods=['GET', 'POST'])
@oidc.require_login
def login():
    return redirect(url_for('stocks.main'))


@stocks_blueprint.route('/register', methods=['GET', 'POST'])
@oidc.require_login
def register():
    return redirect(url_for('stocks.index'))


@stocks_blueprint.route('/remove_stock', methods=['POST'])
@oidc.require_login
def remove_stock():
    if request.method == 'POST':
        try:
            user_id = oidc.user_getfield("sub") if oidc.user_loggedin else None
            if not user_id:
                flash('Please log in to remove stocks', 'alert-danger')
                return redirect(url_for('stocks.login'))
            
            stock_id = request.form['stock_id']
            # Only allow users to delete their own stocks
            stock = StockDb.query.filter_by(id=stock_id, user_id=user_id).first()
            
            if stock:
                db.session.delete(stock)
                db.session.commit()
                flash('Stock removed successfully', 'alert-success')
            else:
                flash('Stock not found or you do not have permission to delete it', 'alert-danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error removing stock: {str(e)}', 'alert-danger')
        
        return redirect(url_for('stocks.main'))


@stocks_blueprint.route('/logout', methods=['POST', 'GET'])
def logout():
    oidc.logout()
    return redirect(url_for('stocks.index'))


@app.route('/')
def base():
    return redirect("/stocks/main", code=302)


@stocks_blueprint.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('stocks/index.html')

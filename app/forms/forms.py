from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError
from wtforms import StringField, SubmitField
from app.models.stock_info import StockInfo


# Cache StockInfo instance to avoid reloading CSV files
_stock_info_cache = None

def _get_stock_info():
    """Get cached StockInfo instance."""
    global _stock_info_cache
    if _stock_info_cache is None:
        _stock_info_cache = StockInfo()
    return _stock_info_cache


def validate_stock_symbol(form, field):
    """Validate that the stock symbol exists in our ticker database."""
    if not field.data:
        raise ValidationError('Stock symbol is required')
    
    try:
        stock_info = _get_stock_info()
        if field.data.upper() not in [stock['symbol'] for stock in stock_info.tickers]:
            raise ValidationError(f'Stock "{field.data}" was not found')
    except Exception as e:
        raise ValidationError(f'Error validating stock symbol: {str(e)}')


def validate_input_isnumeric(form, field):
    """Validate that the input is a valid positive number."""
    if not field.data:
        raise ValidationError('This field is required')
    
    try:
        value = float(field.data)
        if value <= 0:
            raise ValidationError('Please enter a positive number')
    except ValueError:
        raise ValidationError('Please enter numbers only')
    except Exception as e:
        raise ValidationError(f'Invalid input: {str(e)}')


class AddStockForm(FlaskForm):
    stock_symbol = StringField('Stock Symbol',
                               validators=[InputRequired(), validate_stock_symbol])
    purchase_price = StringField('Price at Purchase',
                                 validators=[InputRequired(), validate_input_isnumeric])
    num_of_shares = StringField('Number of Shares',
                                validators=[InputRequired(), validate_input_isnumeric])
    submit = SubmitField('Add Stock')

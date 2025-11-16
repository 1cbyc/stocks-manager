import uuid
from typing import Dict, Optional
from wallstreet import Stock as WS
from app.models.stock_info import StockInfo


class StockError(Exception):
    """Custom exception for stock-related errors"""
    pass


class Stock:

    def __init__(self, stock_symbol: str, number_of_shares: float, purchase_price: float, _id: str = None):
        self._id = _id or uuid.uuid4().hex
        self.number_of_shares = number_of_shares
        self.purchase_price = purchase_price
        self.stock_info = StockInfo()
        self.stock_data = self._add_stock(stock_symbol)

    def _add_stock(self, stock_symbol) -> Dict:
        stock_symbol = stock_symbol.upper()
        
        # Get full name with error handling
        full_name_data = self.stock_info.get_full_name(stock_symbol)
        if not full_name_data or 'company' not in full_name_data:
            raise StockError(f'Stock symbol "{stock_symbol}" not found in database')
        
        # Get logo URL (can be None)
        logo_url = self.stock_info.get_logo_url(stock_symbol)
        
        return dict(
            _id=self._id,
            full_name=full_name_data['company'],
            stock_symbol=stock_symbol,
            shares=float(self.number_of_shares),
            purchase_price=float(self.purchase_price),
            net_buy_price=round(float(self.number_of_shares) * float(self.purchase_price), 2),
            logo=logo_url or ''
        )

    @staticmethod
    def get_current_price_by_symbol(stock_symbol: str) -> float:
        """
        Get current stock price by symbol.
        Raises StockError if stock symbol is invalid or API call fails.
        """
        try:
            upper_stock_symbol = stock_symbol.upper()
            stock = WS(upper_stock_symbol)
            price = stock.price
            
            if price is None or price <= 0:
                raise StockError(f'Invalid price data for stock symbol "{stock_symbol}"')
            
            return float(price)
        except Exception as e:
            if isinstance(e, StockError):
                raise
            raise StockError(f'Failed to fetch price for "{stock_symbol}": {str(e)}')

    @classmethod
    def get_yield_of_single_stock(cls, stock) -> Dict:
        """
        Calculate yield for a single stock.
        Returns dict with profit/loss information, or None if price fetch fails.
        """
        try:
            num_of_shares = stock.shares
            stock_symbol = stock.stock_symbol
            purchase_price = stock.purchase_price
            
            try:
                current_price = cls.get_current_price_by_symbol(stock_symbol)
            except StockError:
                # Return None values if price fetch fails
                return dict(
                    symbol=stock_symbol,
                    profit_in_usd=None,
                    profit_prec=None,
                    total_value=None,
                    error=True
                )

            profit_in_usd = (current_price - purchase_price) * num_of_shares
            profit_prec = (current_price - purchase_price) / purchase_price * 100
            total_value = num_of_shares * current_price

            return dict(
                symbol=stock_symbol,
                profit_in_usd=round(profit_in_usd, 2),
                profit_prec=round(profit_prec, 2),
                total_value=round(total_value, 2),
                error=False
            )
        except Exception as e:
            return dict(
                symbol=getattr(stock, 'stock_symbol', 'UNKNOWN'),
                profit_in_usd=None,
                profit_prec=None,
                total_value=None,
                error=True
            )

    @classmethod
    def get_total(cls, stocks):
        """
        Calculate total portfolio value and profit/loss.
        Handles cases where individual stock prices cannot be fetched.
        """
        quantity = 0
        value = 0
        profit_loss = 0

        for stock in stocks:
            stock_yield = cls.get_yield_of_single_stock(stock)

            quantity += stock.shares
            
            # Only add to totals if price was successfully fetched
            if not stock_yield.get('error', False):
                if stock_yield['total_value'] is not None:
                    value += stock_yield['total_value']
                if stock_yield['profit_in_usd'] is not None:
                    profit_loss += stock_yield['profit_in_usd']

        return dict(
            quantity=round(quantity, 2),
            value=round(value, 2),
            profit_loss=round(profit_loss, 2)
        )

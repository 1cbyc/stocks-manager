from app import db


class StockDb(db.Model):
    """
    Database model for storing user stock portfolio entries.
    Each stock entry is associated with a user_id to support multi-user functionality.
    """
    id = db.Column(db.String(120), primary_key=True)
    user_id = db.Column(db.String(120), nullable=False, index=True)  # Okta user ID
    full_name = db.Column(db.String(120))
    stock_symbol = db.Column(db.String(120), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    net_buy_price = db.Column(db.Float, nullable=False)
    logo = db.Column(db.String(500))  # Increased length for longer URLs
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Unique constraint: prevent duplicate stocks per user
    __table_args__ = (
        db.UniqueConstraint('user_id', 'stock_symbol', name='unique_user_stock'),
    )

    def __repr__(self):
        return f'Stock symbol: {self.stock_symbol}, Shares: {self.shares}, Purchase price: {self.purchase_price}'

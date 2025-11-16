// app/
// ├── models/          # Business logic and data models
// │   ├── stock.py     # Stock class with profit/loss calculations
// │   └── stock_info.py # Loads ticker symbols and logos from CSV
// ├── database/        # Database models
// │   └── database.py  # StockDb SQLAlchemy model
// ├── routes/          # Flask routes/views
// │   └── routes.py    # Main application routes
// ├── forms/           # WTForms definitions
// │   └── forms.py     # AddStockForm with validation
// ├── data/            # Static data files
// │   ├── tickers.csv  # ~4000+ stock symbols and company names
// │   └── logo.csv     # Company logos (Clearbit URLs)
// ├── templates/       # Jinja2 HTML templates
// │   ├── base.html    # Base template with navigation
// │   └── stocks/
// │       ├── index.html  # Landing page
// │       └── table.html  # Portfolio table view
// └── static/          # CSS, JS, images, fonts
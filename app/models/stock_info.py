import csv
import os


class StockInfo:
    """
    Handles stock ticker and logo information.
    Uses class-level caching to avoid reloading CSV files on every instantiation.
    """
    
    # Class-level cache for tickers and logos
    _tickers_cache = None
    _logos_cache = None
    
    def __init__(self):
        # Load data only if not already cached
        if StockInfo._tickers_cache is None:
            StockInfo._tickers_cache = list(self._load_all_tickers())
        if StockInfo._logos_cache is None:
            StockInfo._logos_cache = list(self._load_all_logos())
        
        self.tickers = StockInfo._tickers_cache
        self.logos = StockInfo._logos_cache

    @staticmethod
    def _get_data_path(filename):
        """Get the absolute path to data files."""
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to app/, then into data/
        app_dir = os.path.dirname(current_dir)
        return os.path.join(app_dir, 'data', filename)

    @staticmethod
    def _load_all_tickers():
        """Load all ticker symbols from CSV file."""
        file_path = StockInfo._get_data_path('tickers.csv')
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if len(row) >= 2:  # Ensure row has at least 2 columns
                        yield dict(company=row[0].strip(), symbol=row[1].strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Tickers CSV file not found at: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading tickers CSV: {str(e)}")

    @staticmethod
    def _load_all_logos():
        """Load all logo URLs from CSV file."""
        file_path = StockInfo._get_data_path('logo.csv')
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if len(row) >= 2:  # Ensure row has at least 2 columns
                        yield dict(company=row[0].strip(), logo=row[1].strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Logo CSV file not found at: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading logo CSV: {str(e)}")

    def get_full_name(self, stock_symbol: str) -> dict:
        """Get full company name for a stock symbol.
        
        Args:
            stock_symbol: The stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            dict with 'company' and 'symbol' keys, or None if not found
        """
        if not stock_symbol:
            return None
        
        stock_symbol = stock_symbol.upper()
        for stock in self.tickers:
            if stock['symbol'] == stock_symbol:
                return stock
        return None

    def get_logo_url(self, stock_symbol: str) -> str:
        """Get logo URL for a stock symbol.
        
        Args:
            stock_symbol: The stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Logo URL string, or None if not found
        """
        if not stock_symbol:
            return None
        
        stock_symbol = stock_symbol.upper()
        for logo in self.logos:
            if logo['company'] == stock_symbol:
                return logo['logo']
        return None
    
    @classmethod
    def clear_cache(cls):
        """Clear the cached data (useful for testing or reloading)."""
        cls._tickers_cache = None
        cls._logos_cache = None

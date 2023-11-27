import nasdaqdatalink
import config as config

nasdaqdatalink.ApiConfig.api_key = config.nasdaq_key 


def get_nasdaq_datatable(table_name, ticker_symbol):
    """
    Fetch datatable for a given table name and ticker symbol from Nasdaq Data Link.

    Args:
    - table_name (str): The datatable name (e.g., 'ZACKS/FC').
    - ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
    - DataFrame: A pandas DataFrame containing the datatable data.
    """
    
    # Fetch the data
    data = nasdaqdatalink.get_table(table_name, ticker=ticker_symbol)
    
    return data


# Example usage
table = 'ZACKS/FC'
ticker = 'AAPL'
data = get_nasdaq_datatable(table, ticker)

print(data.head())
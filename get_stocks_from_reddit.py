import asyncio
import string
import unicodedata
import asyncpraw
from collections import Counter
import requests
import config as config

#config variables:
API_KEY = config.alpha_key
client_id = config.client_id 
client_secret = config.client_secret
username = config.username
password = config.password
user_agent = config.user_agent

#create list of the subreddits you want to parse: 
SUBREDDITS_TO_PARSE = ['wallstreetbets', 'stocks', 'investing', 'StockMarket']

#words that may be capitalized but are not stocks: 
KNOWN_NOT_STOCKS = ['UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'LAWSUIT', 'AGAINST', 'VALHALLA', 'MOON', 'PE', 'COVID', 'IMO', 'IPO', 'BTC', 'PUT', 'CALL',
                    'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'I', 'STILL', "DIDN'T", 'HEAR', 'EBITDA', 'SQUEEZE', 'BS', 'VIX', 'FUD', 'HUT', 'ITM', 'OTM',
                    'NO', 'BELL', 'CEO', 'CFO', 'Q1', 'DD', 'MOASS', 'STONK', 'MEME', 'DICK', 'FOMO', 'EV', 'PIPE', 'HOLD', 'OTC', 'NOKPF', 'TTM', 'SPY',
                    'TO', 'A', 'THE', 'FUCK', 'US', 'FUCKING', 'ARE', 'DD', 'US', 'TLDR', 'EDIT', 'IV', 'SP500', 'SEC', 'GLOBE', 'NEWSWIRE', 'PT',
                    'NYSE', 'SPAC', 'FDA', 'DNA', 'HODL', 'USDA', 'PTSD', 'ETF', 'LLC', 'CSE', 'USA', 'EPS', 'BUY', 'B', 'AM', 'PM', 'SI', 'SP', 'TBA', 'TBD']

#create a Reddit instance using the client_id and client_secret from the app we created early
#the 'user_agent' is just a unique identifier for your application that you can make up
#list of words in title and comments
word_collection = []


def remove_punc(text):
    """
    Remove punctuation from a given string.

    Args:
    - text (str): Input string from which punctuation needs to be removed.

    Returns:
    - str: String without punctuation.
    """
    return ''.join(ch for ch in text if ch not in string.punctuation)


def remove_emoji(text):
    """
    Remove emojis from a given string.

    Args:
    - text (str): Input string from which emojis need to be removed.

    Returns:
    - str: String without emojis.
    """
    return ''.join(ch for ch in text if not is_emoji(ch))


def is_emoji(character):
    """
    Check if a given character is an emoji.

    Args:
    - character (str): Input character to be checked.

    Returns:
    - bool: True if character is an emoji, False otherwise.
    """
    return unicodedata.category(character) in ('So', 'Cn')


def containsNumber(text):
    """
    Check if a string contains any numerical digits.

    Args:
    - text (str): Input string to be checked.

    Returns:
    - bool: True if the string contains a number, False otherwise.
    """
    return any(ch.isdigit() for ch in text)


async def get_stocks():
  async with asyncpraw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    username = username,
    password=password,
    user_agent=user_agent,
) as reddit:
    #loop through subreddits
    for sub in SUBREDDITS_TO_PARSE:      
        #create instance of the subreddit class
        subreddit_instance = await reddit.subreddit(sub)
      
        #sort by hot and get the most recent 50 submissions
        # submissions = subreddit_instance.hot(limit=50)

        #loop through submissions, split title, add to list
        async for submission in subreddit_instance.hot(limit=50):
          print(f"submission title: {submission.title}")
          title_words = submission.title.split()
          word_collection.extend(title_words)

          # Ensure the submission is loaded
          await submission._fetch()
          # #get submission comments
          submission.comments.replace_more(limit=0)  # flatten tree
          comments = submission.comments.list()  # all comments
          # print(comments)

          #we can also look through the comments to see what words they contain:
          for top_level_comment in comments[:1]:
            print(f"top_level_comment: {top_level_comment.body.split()}")
            comment_words = top_level_comment.body.split()
            word_collection.extend(comment_words)
    

    #list to hold words that may be stock tickers
    potential_stock_symbols = []
    
    #loop through word_collection, cleanup words, and check if each word is potentially a stock ticker
    for word in word_collection:
      cleaned_word = remove_punc(word)
      cleaned_word = remove_emoji(cleaned_word)
      print(cleaned_word)
      if cleaned_word.isupper() and not containsNumber(cleaned_word) and cleaned_word not in KNOWN_NOT_STOCKS:
          potential_stock_symbols.append(cleaned_word)
    
    print(potential_stock_symbols)

    return potential_stock_symbols
  

def is_valid_stock(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "SYMBOL_SEARCH"
    datatype = "json"

    params = {
        "function": function,
        "keywords": symbol,
        "apikey": API_KEY,
        "datatype": datatype
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    
    print(data)

    # Check if the symbol exists in the search results
    for match in data.get('bestMatches', []):
        if match.get('1. symbol') == symbol:
            return True
    return False


def clean_symbols(symbols):
    unique_symbols = set(symbols)
    valid_symbols = [symbol for symbol in unique_symbols if is_valid_stock(symbol)]
    return valid_symbols


# Example
asyncio.run(get_stocks())
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("FLASK_DEBUG")
FLASK_APP_SECRET_KEY = os.getenv("FLASK_APP_SECRET_KEY")
CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
NUM_TWEETS_TO_GRAB = int(os.getenv("NUM_TWEETS_TO_GRAB") or "1000")
OCP_APIM_SUBSCRIPTION_KEY = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")
TWITTER_FETCHER = os.getenv("TWITTER_FETCHER")
DEFAULT_CACHE_TIMEOUT = int(os.getenv("DEFAULT_CACHE_TIMEOUT") or "3600")

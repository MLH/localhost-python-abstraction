import config
import tweepy

MAX_NUMBER_OF_TWEETS_PER_PAGE = 200
MAX_NUMBER_OF_TWEETS_ALLOWED = 3200

# user authentication to use twitter API
def get_user_auth_twitter():
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except StopIteration:
            return
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


def get_number_of_pages():
    number_of_tweets_config = int(config.NUM_TWEETS_TO_GRAB or "1000")
    max_number_of_tweets_allowed = min(
        MAX_NUMBER_OF_TWEETS_ALLOWED, number_of_tweets_config
    )
    return max_number_of_tweets_allowed / MAX_NUMBER_OF_TWEETS_PER_PAGE


# fetch tweets
def get_tweets(twitter_handle):
    if not twitter_handle:
        return []

    twitter_handle = (
        twitter_handle if twitter_handle.startswith("@") else "@" + twitter_handle
    )

    auth = get_user_auth_twitter()
    api = tweepy.API(auth)

    public_tweets = []

    for tweets in limit_handled(
        tweepy.Cursor(
            api.user_timeline,
            twitter_handle,
            tweet_mode="extended",
            count=MAX_NUMBER_OF_TWEETS_PER_PAGE,
        ).pages(get_number_of_pages())
    ):
        public_tweets.extend(tweets)

    return [tweet._json["full_text"] for tweet in public_tweets]

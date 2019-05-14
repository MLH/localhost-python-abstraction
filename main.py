#!flask/bin/python
from flask import Flask, jsonify, request
import config
from tweets_fetcher import get_tweets
from content_moderator import moderate
from flask_caching import Cache


cache_config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": config.DEFAULT_CACHE_TIMEOUT,
}
cache = Cache(config=cache_config)

app = Flask(__name__)
cache.init_app(app)


# Fetch tweets
@app.route("/api/tweets/<string:twitter_handle>", methods=["GET"])
@cache.cached()
def tweets(twitter_handle):
    if not twitter_handle:
        abort(400)

    return jsonify({"data": get_tweets(twitter_handle)})


# Moderate content
@app.route("/api/moderated_content", methods=["POST"])
@cache.cached()
def content():
    if not request.json or not "content" in request.json:
        abort(400)

    return jsonify({"data": moderate(request.json.get("content", ""))})


if __name__ == "__main__":
    app.run(debug=config.DEBUG)

#!flask/bin/python
from flask import Flask, jsonify, request
import config
from tweets_fetcher import get_tweets
from content_moderator import moderate

app = Flask(__name__)


# Fetch tweets
@app.route("/api/tweets/<string:twitter_handle>", methods=["GET"])
def tweets(twitter_handle):
    if not twitter_handle:
        abort(400)

    return jsonify({"data": get_tweets(twitter_handle)})


# Moderate content
@app.route("/api/moderated_content", methods=["POST"])
def content():
    if not request.json or not "content" in request.json:
        abort(400)

    return jsonify({"data": moderate(request.json.get("content", ""))})


if __name__ == "__main__":
    app.run(debug=config.DEBUG)

import os
from helpers import *
from datetime import datetime
from twitter_text import Autolink
from flask import Flask, request, render_template
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)

@app.template_filter()
def time_since(tweet_time, default="just now"):
    tweet_time = datetime.strptime(tweet_time, '%a, %d %b %Y %H:%M:%S +0100')
    now = datetime.utcnow()
    diff = now - tweet_time
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default

@app.template_filter()
def real_time(tweet_time):
    tweet_time = datetime.strptime(tweet_time, '%a, %d %b %Y %H:%M:%S +0000')
    return tweet_time

@app.template_filter()
def sentiment_highlight(tweet):
    if tweet['polarity'] == 4:
        return 'alert-message block-message success positive'
    elif tweet['polarity'] == 0:
        return 'alert-message block-message error negative'
    elif tweet['polarity'] == 2:
        return 'alert-message block-message info neutral'
    else:
        return 'alert-message block-message warning'

@app.template_filter()
def state_sentiment(tweet):
    if tweet['polarity'] == 4:
        return 'positive'
    elif tweet['polarity'] == 0:
        return 'negative'
    elif tweet['polarity'] == 2:
        return 'neutral'
    else:
        return 'dunno'
        
@app.template_filter()
def autolink(tweet_text):
    return Autolink(tweet_text).auto_link()
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('index.html')

@app.route('/search')
def search():
    print datetime.now(), "get query"
    query = request.args.get('q')
    print datetime.now(), "go for results"
    params = get_results(query)
    print datetime.now(), "get results"
    return render_template('search.html', params=params)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

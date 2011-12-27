import os
from helpers import *
from flask import Flask, request, render_template

app = Flask(__name__)
twitter = Twitter()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = get_tweets(query)
    tagcount = count_tags(tweets)
    sentiment, sent_tweets = get_sentiment(tweets)
    return render_template('search.html', tweets=sent_tweets, 
                            tagcount=tagcount, sentiment=sentiment, len=len)

@app.route('/chart')
def chart():
    return render_template('chart.html')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

import os
from helpers import *
from twitter import *
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
    tweets = []
    for page in range(1, 2):
        tweets += twitter.search(q=query, rpp=100, page=page)['results']
    tagcount = count_tags(tweets)
    sentiment = aggregate_sentiment(tweets)
    return render_template('search.html', tweets=tweets, tagcount=tagcount, 
                    sentiment=sentiment, len=len, get_sentiment=get_sentiment)

@app.route('/chart')
def chart():
    return render_template('chart.html')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

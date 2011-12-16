import os
from flask import Flask, request, render_template
from twython import Twython
from twitter_text import Autolink
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    twitter = Twython()
    results = twitter.searchTwitter(q=query)
    return render_template('search.html', results=results, Autolink=Autolink)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

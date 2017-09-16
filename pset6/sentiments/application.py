from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    
    poscount = 0
    negcount = 0
    neucount = 0
    
    analyzer = Analyzer("positive-words.txt", "negative-words.txt")
    
    for i in range(len(tweets)):
        score = analyzer.analyze(tweets[i])
        if score > 0.0:
            poscount += 1
        elif score < 0.0:
            negcount += 1
        else:
            neucount += 1
            
    
            
    if poscount == 0 and negcount == 0 and neucount == 0:
        print("User has no tweets")
        neucount = 100
    else:
        poscount = float((poscount / len(tweets)) * 100)
        negcount = float((negcount / len(tweets)) * 100)
        neucount = float((neucount / len(tweets)) * 100)

    

    positive, negative, neutral = poscount, negcount, neucount

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)

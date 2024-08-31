from flask import Flask,render_template,request
import google.generativeai as palm
import random
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
palm.configure(api_key=API_KEY)
print("API_KEY " + API_KEY)
model = {"model": "models/text-bison-001"}
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/financial_FAQ",methods=["GET","POST"])
def financial_FAQ():
    return(render_template("financial_FAQ.html"))

@app.route("/makersuite",methods=["GET","POST"])
def makersuite():
    q = request.form.get("q")
    r = palm.chat(messages=q, **model)
    return(render_template("makersuite.html",r=r.last))

jokes = [
    "Why couldn't encik order McSpicy upsize? Because he's a regular.",
    "Why trees unlucky? Cos they sway.",
    "Which noodle is the heaviest? Wanton (one-tonne) noodle.!",
    "How you come here? I take bus 11 (2 legs)",
    "BreadTalk and Kopitiam, who is more talkative? BreadTalk, because Bread talk, Kopi tiam.",
    "What did the Singapore Airlines air stewardess say when a passenger blocked her way? SQ me!",
    "Which is the tallest building in Singapore? – The National Library, because it has many stories."
]

@app.route("/joke",methods=["GET","POST"])
def joke():
    joke = random.choice(jokes)
    return render_template('joke.html', joke=joke)

if __name__ == "__main__":
    app.run()
from flask import Flask,render_template,request
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv
import joblib
import sklearn

load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)
#print("API_KEY " + API_KEY)
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/financial_FAQ",methods=["GET","POST"])
def financial_FAQ():
    return(render_template("financial_FAQ.html"))

model = {"model": "models/text-bison-001"}

@app.route("/makersuite",methods=["GET","POST"])
def makersuite():
    model = genai.GenerativeModel('gemini-1.5-flash')
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("makersuite.html", r=r.text))

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

predictionmodel = joblib.load('model/dbs_model.jl')

@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    predicted_price = None
    if request.method == 'POST':
        try:
            # Get the input value from the form
            sgd_value = float(request.form['sgd_value'])

            # Make a prediction using the loaded model
            predicted_price = predictionmodel.predict([[sgd_value]])

        except Exception as e:
            print("Error during prediction:", e)
            return "Bad Request: " + str(e), 400

    return render_template('prediction.html', predicted_price=predicted_price)


if __name__ == "__main__":
    app.run()
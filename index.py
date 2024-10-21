import os
import requests
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

#####################
## Get the API Key ##
#####################
# From environmental varaiables
apikey = os.environ.get("GOOGLE_API_KEY", None)

# From apikey.txt file
if not apikey:
    with open("./apikey.txt") as f:
        apikey = f.read()
        if apikey == "<WRITE IN YOUR GEMINI API KEY HERE>":
            raise Exception("You did not put your google api key into apikey.txt")



@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/answer', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':

        userResume = request.form.get("resume")
        userResume = "Below is my resume:\n" + userResume

        userJobDescription = request.form.get("job_description")
        userJobDescription = "Write me a 300 word maximum cover letter for the job desciption below:\n" + userJobDescription

        finalText = userResume + "\n" + userJobDescription
        API_KEY = apikey
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        data = {
            "contents": [
                {"parts": [{"text": finalText}]}
            ]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(URL, json=data, headers=headers)
        json = response.json()
        
        
        try:
            print(json['candidates'][0]['content']['parts'][0]['text'])
            data = json['candidates'][0]['content']['parts'][0]['text']
        except:
            print(json)
            data = json
        return render_template("answer.html", data=data, error=error)
    
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
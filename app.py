from flask import Flask, request, render_template, redirect, url_for
from ibm_watson_machine_learning import APIClient

app = Flask(__name__)

# IBM Watson credentials
wml_credentials = {
    "apikey": "8LqEsfxH0lAXFHDN_bTELo3aTQkOJ4IAqOeSlMescJTg",
    "url": "https://eu-de.ml.cloud.ibm.com"
}
client = APIClient(wml_credentials)

# Set the default space
SPACE_ID = "9ba155c3-886a-4b9b-b70d-c4a8a2529cf4"
client.set.default_space(SPACE_ID)

DEPLOYMENT_ID = "e19d49f0-f554-4b75-af67-30038365d9af"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = {
        "id": int(request.form.get("id")),
        "A1_Score": int(request.form.get("A1_Score")),
        "A2_Score": int(request.form.get("A2_Score")),
        "A3_Score": int(request.form.get("A3_Score")),
        "A4_Score": int(request.form.get("A4_Score")),
        "A5_Score": int(request.form.get("A5_Score")),
        "A6_Score": int(request.form.get("A6_Score")),
        "A7_Score": int(request.form.get("A7_Score")),
        "A8_Score": int(request.form.get("A8_Score")),
        "A9_Score": int(request.form.get("A9_Score")),
        "A10_Score": int(request.form.get("A10_Score")),
        "age": int(request.form.get("age")),
        "gender": request.form.get("gender"),
        "ethnicity": request.form.get("ethnicity"),
        "jundice": request.form.get("jundice"),
        "contry_of_res": request.form.get("contry_of_res"),
        "used_app_before": request.form.get("used_app_before"),
        "result": int(request.form.get("result")),
        "age_desc": request.form.get("age_desc"),
        "relation": request.form.get("relation"),
        "Class/ASD": request.form.get("Class/ASD"),
    }

    payload_scoring = {
        "input_data": [
            {
                "fields": list(input_data.keys()),
                "values": [list(input_data.values())]
            }
        ]
    }

    try:
        response_scoring = client.deployments.score(
            deployment_id=DEPLOYMENT_ID,
            meta_props=payload_scoring
        )
        prediction = response_scoring['predictions'][0]['values'][0][0]
        return render_template("result.html", prediction=prediction)
    except Exception as e:
        return f"Error: {str(e)} <br><a href='/home'>Go Back</a>"

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
import logging


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    html = f"<h3>Hi This is Udacity DevOps Capstone Project</h3>"
    return html.format(format)
    
@app.route("/about")
def index():
    return render_template("about.html")

@app.route("/api", methods=['POST'])
def predict():
    # Logging the input payload
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload}")
    return jsonify({'payload': "Thank you !!"})

if __name__ == "__main__":
    # start server
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80

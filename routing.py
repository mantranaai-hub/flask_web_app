from flask import Flask,render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/",methods=['GET'])
def homepage():
    return render_template("homepage.html")


@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/landpage",methods=["POST"])
def landpage():
    return "Welcome to my website, Its a AI enabled website."

@app.route("/candidate_login", methods=['POST'])
def can_login():
    print("candidate login")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)

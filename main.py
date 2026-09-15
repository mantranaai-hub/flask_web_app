from flask import Flask, render_template, request, redirect, url_for
'''
It creates the Flask instance
which will be your WSGI (web server gateway interface) application
'''

app=Flask(__name__)

'''something like creating the homepage, 
when ever I will use / along with the URL than I will be
landed in the home page.'''

@app.route(rule = "/")
def welcome():
    return """
<html>
    <body>
        <h1>Welcome to Generative AI</h1>

        <h2>Large Language Models</h2>
        <p>LLMs learn patterns from large amounts of text.</p>
        <p>They can generate, summarize, and understand human language.</p>

        <h2>Diffusion Models</h2>
        <p>Diffusion models create images by gradually removing noise.</p>
        <p>They power tools that generate images from text prompts.</p>
    </body>
</html>
"""

@app.route(rule="/index")
def index():
    return render_template(
        "index.html",
        index="LLMs understand and generate text, while diffusion models generate images."
    )

@app.route(rule="/form", methods=['GET','POST'])
def form():
    if request.method=='POST':
        name = request.form['name']
        return f"Hi {name}! Welcome to the my website"
    return render_template("form.html")

@app.route(rule="/submit",methods=['POST'])
def submit():
    if request.method=='POST':
        name = request.form['name']
        return f"Hi {name}! Welcome to the my website"

# variable rule

@app.route(rule="/sucess/<int:score>")
def sucess(score:int):
    return "The mark is " + str(score)

@app.route(rule="/sucessfor/<int:score>")
def sucessfor(score:int):
    return "The mark is " + str(score)

@app.route(rule="/sucessif/<int:score>")
def sucessif(score:int):
    return "The mark is " + str(score)

# print(__name__)

if __name__=="__main__":
    app.run(debug=True)

# HTTP verb

"""
GET: When we hit a URL, the server will return back with a page or content, (www.google.com), we will get a web page back.
POST: When we search or enter some information in the web page, the data will be retreived from the back end and showed.
--------------------------

# Building URL Dynamically:
# variable rule
# Jinja 2 Template Engine
    {{ }}: where we can pass the value directly from the back end. single value
    {%...%}: can be sued to do for loop/If
    {#...#}: single line comment

"""
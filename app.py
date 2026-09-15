from flask import Flask
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
    return "Welcome to the wellcome page"

@app.route(rule="/index")
def index():
    return "Welcome to index page"
# print(__name__)





if __name__=="__main__":
    app.run(debug=True)


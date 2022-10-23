from fileinput import filename
from flask import Flask, render_template


app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/static/{path}')
def aboutCss(path):
    with open(path) as f:
        return f.read()

@app.route('/game')
def index2():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7878)

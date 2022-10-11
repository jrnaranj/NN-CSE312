from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def index2():
    return render_template('index2.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7878)

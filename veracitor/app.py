
from flask import Flask, render_template

# configuration

app = Flask(__name__)
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

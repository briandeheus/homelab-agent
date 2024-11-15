from flask import Flask, render_template

from lib.git import get_short_commit_hash

app = Flask(__name__)


@app.route("/")
def home():
    github_commit = get_short_commit_hash()
    return render_template("landing.html", github_commit=github_commit)


if __name__ == "__main__":
    app.run(debug=True)

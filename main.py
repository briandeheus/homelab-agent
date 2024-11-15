from flask import Flask, render_template

from lib.git import get_short_commit_hash
from lib.system import (
    get_cpu_usage,
    get_hostname,
    get_memory_usage,
    get_network_usage,
    get_temperature,
    get_uptime,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "landing.html",
        github_commit=get_short_commit_hash(),
        hostname=get_hostname(),
        uptime=get_uptime(),
        temperature=get_temperature(),
        cpu_usage=get_cpu_usage(),
        memory=get_memory_usage(),
        network=get_network_usage(),
    )


if __name__ == "__main__":
    app.run(debug=True)

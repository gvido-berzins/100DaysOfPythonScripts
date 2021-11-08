from time import sleep

from flask import (
    Flask, render_template, render_template_string, stream_with_context
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    @stream_with_context
    def generate():
        yield render_template_string(
            '<link rel=stylesheet href="{{ url_for("static", filename="stream.css") }}">'
        )

    for i in range(500):
        anchor = f"scroll{i}"

        yield render_template_string(
            "<p id='{{ scroll }}'>{{ i }}: {{ s }}</p>n",
            i=i,
            s=i * i,
            scroll=anchor
        )
        sleep(0.1)

    return app.response_class(generate())


app.run(debug=True)

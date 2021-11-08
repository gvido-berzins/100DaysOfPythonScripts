import datetime
from time import sleep

import werkzeug
from flask import Flask, Response, render_template

app = Flask(__name__)

JAVASCRIPT = """
let id = 0;
function scrollTo(id) { const el = document.getElementById(id); el.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"}); }
window.setInterval(function() { if (id != -999) { scrollTo(id); }; }, 200);
"""


@app.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")


def flask_logger():
    """creates logging information"""
    for i in range(100):
        current_time = datetime.datetime.now().strftime("%H:%M:%S") + "\n"
        data = "data" + str(i - 2)
        script = (
            '<script>document.getElementById("%s").scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});</script>'
            % data
        )
        inject = f'<p id="data{i}">{i}: </p>'
        msg = werkzeug.utils.unescape(inject + current_time)
        yield msg.encode()
        sleep(0.5)


@app.route("/log_stream", methods=["GET"])
def log_stream():
    """returns logging information"""
    return Response(
        flask_logger(),
        mimetype="text/html",
        content_type="text/event-stream"
    )


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=9999)

from flask import Flask, render_template, request, Response
import time
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def logs():
    if request.method == "POST":
        return Response(stream_with_context(my_tool()), mimetype='text/html')
    return render_template("index.html")

from flask import stream_with_context

def my_tool():
    yield "Starting tool...<br/>\n"
    time.sleep(2)
    yield "Executing tool...<br/>\n"
    time.sleep(5)
    yield "Tool execution complete.<br/>\n"
    time.sleep(1)
    yield "✅ Tool executed successfully!<br/>\n"
    return "Tool execution finished."

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
from sniffer import SnifferController

app = Flask(__name__)
controller = SnifferController()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "start" in request.form:

            selected_bands = request.form.getlist("band")
            controller.start_sniff_machine()
            

            for band in selected_bands:
                channel = request.form.get(f"channel_{band}")
                controller.start_band(band, channel)

        if "stop" in request.form:
            controller.stop_all()
            controller.stop_sniff_machine()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

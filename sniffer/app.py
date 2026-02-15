from flask import Flask, render_template, request, jsonify
from sniffer import SnifferController, get_logs, add_log

app = Flask(__name__)
controller = SnifferController()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "start" in request.form:
            add_log("User initiated: Start Sniffing")
            selected_bands = request.form.getlist("band")
            
            if not selected_bands:
                add_log("No bands selected", "WARNING")
            else:
                add_log(f"Starting sniff on bands: {', '.join(selected_bands)}")
                controller.start_sniff_machine()
                
                for band in selected_bands:
                    channel = request.form.get(f"channel_{band}")
                    if channel:
                        add_log(f"Configuring {band} with channel {channel}")
                        controller.start_band(band, channel)
                    else:
                        add_log(f"No channel specified for {band}", "WARNING")

        if "stop" in request.form:
            add_log("User initiated: Stop Sniffing")
            controller.stop_all()
            controller.stop_sniff_machine()

    logs = get_logs()
    return render_template("index.html", logs=logs)

@app.route("/api/logs", methods=["GET"])
def fetch_logs():
    """API endpoint to fetch logs for AJAX updates"""
    return jsonify({"logs": get_logs()})

if __name__ == "__main__":
    add_log("Starting Flask web server on http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)

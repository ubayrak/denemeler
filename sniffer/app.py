from flask import Flask, render_template, request, jsonify, send_file
import os
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
    capture_files = controller.get_capture_files()
    sniffing_active = controller.is_sniffing_active()
    return render_template("index.html", logs=logs, capture_files=capture_files, sniffing_active=sniffing_active)

@app.route("/api/logs", methods=["GET"])
def fetch_logs():
    """API endpoint to fetch logs for AJAX updates"""
    return jsonify({"logs": get_logs()})

@app.route("/download/<filename>")
def download_file(filename):
    """Download a capture file"""
    try:
        # Ensure the filename is safe and only contains allowed characters
        if not filename.endswith('.pcap') or '/' in filename or '..' in filename:
            return "Invalid filename", 400
        
        # Get the current working directory and construct the file path
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)
        
        # Check if file exists
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            add_log(f"Download failed: File {filename} not found", "WARNING")
            return f"File {filename} not found", 404
            
    except Exception as e:
        add_log(f"Download error for {filename}: {str(e)}", "ERROR")
        return "Download failed", 500

if __name__ == "__main__":
    add_log("Starting Flask web server")
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)

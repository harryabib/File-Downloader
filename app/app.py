from flask import Flask, jsonify, render_template, send_file
import os
from datetime import datetime
import magic

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="ok"), 200


def parsed_size(bytes_size):
    if bytes_size == 0:
        return "0 octet"

    units = ["octets", "Ko", "Mo", "Go", "To", "Po"]

    size = float(bytes_size)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.1f} {units[unit_index]}"


def get_files():
    dir_path = "files"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    files = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            size = parsed_size(os.path.getsize(file_path))
            modified = os.path.getmtime(file_path)
            file_info = {
                "name": file_name,
                "size": size,
                "modified": datetime.fromtimestamp(modified).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "type": magic.from_file(file_path, mime=True),
            }
            files.append(file_info)
    return files


@app.route("/", methods=["GET"])
def home():
    files = get_files()
    return render_template("index.html", files=files)


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    print(f"Requested download for: {filename}")
    dir_path = "files"
    file_path = os.path.join(dir_path, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return "File not found", 404


@app.route("/api/files", methods=["GET"])
def json_response():
    return jsonify(get_files())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

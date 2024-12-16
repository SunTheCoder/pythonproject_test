from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

app = Flask(__name__)

# Explicitly allow CORS for your frontend origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

# In-memory storage for uploaded files (temporary testing)
uploaded_files = []


@app.route("/upload", methods=["POST"])
def upload_to_pinata():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    try:
        files = {"file": (file.filename, file)}
        response = requests.post(PINATA_UPLOAD_URL, headers=headers, files=files)

        if response.status_code == 200:
            data = response.json()
            cid = data.get("IpfsHash")
            gateway_url = f"https://gateway.pinata.cloud/ipfs/{cid}"

            # Save metadata to in-memory list
            file_metadata = {
                "filename": file.filename,
                "IpfsHash": cid,
                "PinSize": data.get("PinSize"),
                "Timestamp": data.get("Timestamp"),
                "GatewayURL": gateway_url
            }
            uploaded_files.append(file_metadata)  # Append file metadata

            return jsonify(file_metadata), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/file/<cid>", methods=["GET"])
def get_file_url(cid):
    """
    Returns the gateway URL for the given CID.
    """
    try:
        gateway_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        return jsonify({"GatewayURL": gateway_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/files", methods=["GET"])
def get_all_files():
    """
    Returns all uploaded file metadata.
    """
    return jsonify({"files": uploaded_files}), 200


if __name__ == "__main__":
    app.run(debug=True)

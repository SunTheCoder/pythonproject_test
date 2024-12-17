from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, FileMetadata  # Import from models
import requests
import os

# Load environment variables
load_dotenv()

# Pinata configurations
PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


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

            # Save metadata to the database
            file_metadata = FileMetadata(
                filename=file.filename,
                IpfsHash=cid,
                PinSize=data.get("PinSize"),
                Timestamp=data.get("Timestamp"),
                GatewayURL=gateway_url
            )
            db.session.add(file_metadata)
            db.session.commit()

            return jsonify(file_metadata.to_dict()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/file/<cid>", methods=["GET"])
def get_file_by_cid(cid):
    try:
        file_metadata = FileMetadata.query.filter_by(IpfsHash=cid).first()
        if not file_metadata:
            return jsonify({"error": "File not found"}), 404
        return jsonify(file_metadata.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/files", methods=["GET"])
def get_all_files():
    try:
        all_files = FileMetadata.query.all()
        return jsonify({"files": [file.to_dict() for file in all_files]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

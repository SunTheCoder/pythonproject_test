from . import db

class FileMetadata(db.Model):
    __tablename__ = 'file_metadata'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    IpfsHash = db.Column(db.String(255), nullable=False, unique=True)
    PinSize = db.Column(db.Integer, nullable=True)
    Timestamp = db.Column(db.String(255), nullable=True)
    GatewayURL = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "IpfsHash": self.IpfsHash,
            "PinSize": self.PinSize,
            "Timestamp": self.Timestamp,
            "GatewayURL": self.GatewayURL
        }

import { useState } from "react";
import axios from "axios";

const UploadComponent = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);

  const changeHandler = (event) => {
    setSelectedFile(event.target?.files?.[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      console.log("No file selected");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Upload success:", response.data);
      setUploadResult(response.data); // Store upload result
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
      <h2>Upload File</h2>
      <label>
        Choose File:
        <input type="file" onChange={changeHandler} />
      </label>
      <button onClick={handleUpload}>Upload</button>

      {uploadResult && (
        <div>
          <p>Upload Successful!</p>
          <p>
            CID: <strong>{uploadResult.IpfsHash}</strong>
          </p>
          <a href={`https://gateway.pinata.cloud/ipfs/${uploadResult.IpfsHash}`} target="_blank" rel="noreferrer">
            View File on IPFS
          </a>
        </div>
      )}
    </div>
  );
};

export default UploadComponent;

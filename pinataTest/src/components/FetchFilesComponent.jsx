import { useState } from "react";
import axios from "axios";

const FetchFilesComponent = () => {
  const [cid, setCid] = useState(""); // CID input
  const [fileUrl, setFileUrl] = useState(null);
  const [allFiles, setAllFiles] = useState([]); // State for all files

  // Fetch single file by CID
  const handleFetchByCID = async () => {
    if (!cid) {
      console.log("No CID provided");
      return;
    }

    try {
      const response = await axios.get(`http://127.0.0.1:5000/file/${cid}`);
      setFileUrl(response.data.GatewayURL);
    } catch (error) {
      console.error("Error fetching file URL:", error);
    }
  };

  // Fetch all files
  const handleFetchAll = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/files");
      console.log("Fetched all files:", response.data);
      setAllFiles(response.data.files);
    } catch (error) {
      console.error("Error fetching all files:", error);
    }
  };

  return (
    <div>
      <h2>Fetch File from IPFS</h2>

      {/* Fetch Single File */}
      <label>
        Enter CID:
        <input
          type="text"
          value={cid}
          onChange={(e) => setCid(e.target.value)}
          placeholder="Enter CID here"
        />
      </label>
      <button onClick={handleFetchByCID}>Fetch File by CID</button>

      {fileUrl && (
        <div>
          {/* <h3>Fetched File:</h3>
          <img src={fileUrl} alt="Fetched file" style={{ maxWidth: "300px" }} /> */}
          <p>
            <a href={fileUrl} target="_blank" rel="noreferrer">
              View File on IPFS
            </a>
          </p>
        </div>
      )}

      {/* Fetch All Files */}
      <h2>All Uploaded Files</h2>
      <button onClick={handleFetchAll}>Fetch All Files</button>

      {allFiles.length > 0 && (
        <ul>
          {allFiles.map((file, index) => (
            <li key={index}>
              <p>
                <strong>{file.filename}</strong>
                <br />
                <a href={file.GatewayURL} target="_blank" rel="noreferrer">
                  View on IPFS
                </a>
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FetchFilesComponent;

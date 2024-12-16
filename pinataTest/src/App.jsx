import UploadComponent from "./components/UploadComponent";
import FetchFilesComponent from "./components/FetchFilesComponent";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Pinata IPFS App</h1>
      <UploadComponent />
      <hr />
      <FetchFilesComponent />
    </div>
  );
}

export default App;

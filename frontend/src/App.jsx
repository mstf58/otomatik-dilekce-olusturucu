import React, { useState } from "react";
import './styles/App.css';


const App = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    const response = await fetch("http://127.0.0.1:8000/generate-petition", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Otomatik Dilekçe Oluşturucu</h1>
      <textarea
        rows="6"
        style={{ width: "100%" }}
        value={text}
        onChange={(e) => setText(e.target.value)}
      ></textarea>
      <br />
      <button onClick={handleGenerate}>Dilekçeyi Oluştur</button>

      {loading && <p>İşlem yapılıyor...</p>}

      {result && (
  <div style={{ background: "#f5f5f5", padding: "20px", marginTop: "20px" }}>
 
    <p><strong>Dilekçe:</strong></p>
    <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
      {result.dilekçe}
    </pre>
  </div>
)}

    </div>
  );
};

export default App;

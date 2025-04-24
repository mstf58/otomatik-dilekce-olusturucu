import React, { useState } from "react";
import generatePetition from "../api/GeneratePetition";
import suggestType from "../api/SuggestType";

const PetitionForm = () => {
  const [text, setText] = useState("");
  const [suggestion, setSuggestion] = useState(null);
  const [confirmed, setConfirmed] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSuggest = async () => {
    setLoading(true);
    const response = await suggestType(text);
    setSuggestion(response);
    setConfirmed(false);
    setLoading(false);
  };

  const handleConfirm = async () => {
    setLoading(true);
    const response = await generatePetition(text);
    setResult(response);
    setLoading(false);
  };

  return (
    <div>
      <textarea
        rows="5"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Şikayetinizi buraya yazın..."
        style={{ width: "100%" }}
      />
      <br />
      <button onClick={handleSuggest} disabled={loading}>
        {loading ? "Yükleniyor..." : "Dilekçe Türü Öner"}
      </button>

      {suggestion && !confirmed && (
        <div style={{ marginTop: 10 }}>
          <strong>Önerilen Dilekçe Türü:</strong> {suggestion.onerilen_tur}
          <br />
          <button onClick={handleConfirm}>Bu türle dilekçeyi oluştur</button>
        </div>
      )}

      {confirmed && result && (
        <div style={{ marginTop: 20, background: "#f5f5f5", padding: 10 }}>
          <h3>Oluşan Dilekçe:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default PetitionForm;
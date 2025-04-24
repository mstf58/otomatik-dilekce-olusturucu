const suggestType = async (text) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/suggest-type", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Hata oluştu:", error);
      return { hata: "Tür önerisi yapılamadı." };
    }
  };
  
  export default suggestType;
  
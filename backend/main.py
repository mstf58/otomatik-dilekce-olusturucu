from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from iointel import Agent, Workflow

# API Anahtarı
os.environ["OPENAI_API_KEY"] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjhmOThhZTMyLWJjNjEtNDU1ZC04OGExLTQzOTk0MzQ0ZGU4NiIsImV4cCI6NDg5Nzk2ODIyMH0.O5MSTKBdgBWm4t-_1lD6zQu20du86bsukX69iOClUnHiCRWw4frO_q8UtgReXGV9jplodowUt3UjniiAW7Ddqw"

app = FastAPI()

# CORS: Frontend erişimi için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PetitionRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "API çalışıyor!"}

@app.post("/generate-petition")
def generate_petition(data: PetitionRequest):
    text = data.text

    ### 1. NER Agent
    ner_agent = Agent(
        name="NER Agent",
        instructions="Metinden kişi, kurum, yer, tarih, olay çıkar",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    )
    ner_workflow = Workflow(text=text, client_mode=False)
    ner_result = ner_workflow.extract_categorized_entities(agents=[ner_agent]).run_tasks()

    entities = ner_result.get("results", {}).get("extract_categorized_entities", {})
    davaci = entities.get("persons", ["Davacı Bilinmiyor"])[0]
    davali = entities.get("organizations", ["Davalı Bilinmiyor"])[0]
    tarih = entities.get("dates", ["Tarih Bilinmiyor"])[0]

    ### 2. Classification Agent (Dava türü belirleme)
    class_agent = Agent(
        name="Classifier",
        instructions="Verilen metne göre dava türünü belirle."
                     "Sadece şunlardan birini döndür: Okul, İş başvuru, Şikayet, Banka, Öğrenci, Velayet, Temyiz, Tapu tescil",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    )
    class_workflow = Workflow(text=text, client_mode=False)
    class_result = class_workflow.classify(
        classify_by=[
            ("Okul", "Okul dilekçesi"),
            ("İş başvuru", "İş başvuru dilekçesi"),
            ("Şikayet", "Şikayet dilekçesi"),
            ("Banka", "Banka dilekçesi"),
            ("Öğrenci", "Öğrenci dilekçesi"),
            ("Velayet", "Velayet dilekçesi"),
            ("Temyiz", "Temyiz dilekçesi"),
            ("Tapu tescil", "Tapu tescil dilekçesi")
        ],
        agents=[class_agent]
    ).run_tasks()
    dava_turu = class_result["results"]["classify"][0][0]

    ### 3. Kurum Tahmini
    makam_agent = Agent(
        name="Makam Agent",
        instructions="Bu metne göre dilekçenin gönderileceği kurumu (örneğin: Kaymakamlık, Belediye, Savcılık, Okul Müdürlüğü) tahmin et.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    )
    makam_workflow = Workflow(text=text, client_mode=False)
    makam_result = makam_workflow.custom(
        name="makam-predict",
        objective="dilekçenin gönderileceği yeri tahmin et",
        instructions="Sadece makam adını yaz. Örn: Savcılık, Belediye, Kaymakamlık vs.",
        agents=[makam_agent]
    ).run_tasks()
    makam = makam_result["results"]["makam-predict"].strip()

    ### 4. Dilekçeyi oluşturma (Kurumsal ve düzgün Türkçeyle)
    prompt = f"""
    Sen bir hukuk danışmanısın. Aşağıda bilgileri verilen bir kişi, ilgili kuruma resmi bir dilekçe yazmak istemektedir. 
    Dilekçeyi birinci tekil şahıs (ben dili) ile, resmi ve Türkçeye uygun şekilde yaz.

    Gönderilecek Makam: {makam}
    Davacı: {davaci}
    Davalı: {davali}
    Tarih: {tarih}
    Olay Özeti: {text}
    Dava Türü: {dava_turu}

    Kurumsal ve açık şekilde ifade edilmiş, giriş-paragraf-talep şeklinde yapılandırılmış resmi bir dilekçe hazırla. 
    Türkçe dışı ifadeler, bozuk karakterler, semboller veya kod içerikleri kesinlikle yer almasın.
    """

    petition_agent = Agent(
        name="Petition Writer",
        instructions="Türkçe resmi dilekçe yaz.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    )
    petition_workflow = Workflow(text=prompt, client_mode=False)
    petition_result = petition_workflow.custom(
        name="dilekce-yazdir",
        objective="Türkçe dilekçe hazırla",
        instructions="Kurumsal, açık, düzgün yazılmış bir dilekçe oluştur.",
        agents=[petition_agent]
    ).run_tasks()

    return {
        "makam": makam,
        "davacı": davaci,
        "davalı": davali,
        "tarih": tarih,
        "dava_türü": dava_turu,
        "dilekçe": petition_result["results"]["dilekce-yazdir"]
    }

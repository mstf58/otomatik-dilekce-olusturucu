# Dijital Dilekçe Oluşturucu

Bu proje, kullanıcıların şikayet, başvuru veya resmi taleplerini dilekçe formatında oluşturmalarını sağlayan bir yapay zeka destekli web uygulamasıdır. 
Uygulama IO.NET altyapısı ile geliştirilmiştir ve kullanıcının yazdığı metne uygun olarak otomatik dilekçe oluşturur.

## Özellikler

- Kullanıcıdan alınan metinden:
  - Davacı, davalı, tarih gibi bilgilerin otomatik çıkarılması (NER)
  - Dava türünün sınıflandırılması (Classifier)
  - Makam kurumunun tahmin edilmesi (Makam Agent)
  - Kurumsal dilekçe metninin resmi formatta yazılması (Petition Writer)
- Gelişmiş frontend ile responsive arayüz
- Kopyalanabilir çıktı

## Teknolojiler
- **Frontend**: React.js, Tailwind CSS
- **Backend**: FastAPI
- **AI Altyapısı**: IO.NET Agents API
- **Dil Modeli**: LLaMA 3 70B (Meta)

## Nasıl çalışır?
1. Kullanıcıdan metin alınır.
2. Backend tarafında:
   - Named Entity Recognition (NER)
   - Classifier (Dava türü)
   - Makam tahmini
   - Dilekçe oluşturma
3. Dilekçe frontend'de gösterilir.

## Kurulum
```bash
# frontend
cd frontend
npm install
npm start

# backend
cd backend
uvicorn main:app --reload
```

## Örnek Kullanım
"Şu tarihte, şu şehirde ev sahibim beni evden çıkarmak istedi"

diyen kullanıcı için otomatik olarak resmi ve yasal dilekçe metni oluşturulur.

## Katkıda Bulunanlar
- Mustafa Şahin (OSTİM Teknik Üniversitesi)
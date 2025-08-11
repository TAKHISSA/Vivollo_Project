
# Vivollo AI – LLM ile Semantik Etiketleme & Doğruluk Analizi

## 📌 Proje Amacı
Vivollo AI projesinin amacı, **LLM tabanlı semantik etiketleme sistemi** kurmak ve bu sistemin doğruluğunu manuel etiketleme ile karşılaştırmaktır.  
Bu sayede, **doğru prompt yapısını** ve **en iyi LLM kullanım stratejilerini** keşfetmek hedeflenmektedir.

Proje kapsamında:
- Sohbet mesajları **LLM** ile analiz edilir.
- Her mesaj için şu etiketler üretilir:
  - **Sentiment**: Pozitif / Negatif / Nötr
  - **Konu**: (Örn. Düğün mekanı, Fotoğrafçı, Gelinlik…)
  - **Bot Yanıtladı mı?**: Evet / Hayır
- Aynı veriler **manuel olarak etiketlenir** (ground truth).
- LLM çıktıları ile manuel etiketler karşılaştırılır.
- Doğruluk oranı raporlanır.

---

## 🧭 Proje Akışı
1. **Veri Hazırlama**  
   - Sohbet mesajları `.json` formatında alındı.
   - Manuel etiketleme yapılarak `manual_labels.csv` dosyası oluşturuldu.
   
2. **LLM ile Etiketleme**  
   - GPT-4o-mini kullanılarak etiketler üretildi.
   - LLM çıktıları `data/llm_outputs.json` dosyasında saklandı.

3. **Karşılaştırma & Doğruluk Analizi**  
   - `scripts/analyze_results.py` ile LLM ve manuel etiketler karşılaştırıldı.
   - Her bir başlık (sentiment, konu, bot yanıtı) için doğru/yanlış sayıları ve doğruluk yüzdeleri gibi bilgiler saklandı.

4. **Raporlama**  
   - Doğruluk raporu (`accuracy_report.md`) ve en iyi sonuç veren prompt (`system_prompts.txt`) kaydedildi.

---

## ⚠️ Karşılaşılan Sorunlar ve Çözümler
### 1. **Eşleşmeyen Mesajlar**
- LLM toplam **23.566 mesaj** işledi ancak manuel etiketleme verisinde sadece **4.650 mesaj** bulundu.
- Bu farkın nedeni:
  - Bazı mesajların LLM çıktısında bulunup manuel etiketlerde olmaması.
  - Mesaj metinlerinin küçük farklarla (noktalama, boşluk, emoji, markdown biçimi) farklı olması.
  - Boş string veya gereksiz satırların veride bulunması.

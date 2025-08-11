from openai import OpenAI
import json
import os
import time
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
API_DELAY = 0.3  # Daha hızlı yanıt için bekleme süresi

def load_system_prompt():
    """Sistem promptunu yükler ve JSON kelimesini ekler"""
    try:
        with open('/Users/Hp/Desktop/Vivollo_project/prompts/system_prompts.txt', 'r', encoding='utf-8') as file:
            base_prompt = file.read()
    except Exception as e:
        print(f"Prompt yükleme hatası: {e}")
        base_prompt = """
        Sen bir düğün organizasyon sohbet analiz uzmanısın. Mesajları şu şekilde etiketle:
        1. Sentiment: Pozitif/Negatif/Nötr
        2. Konu: Düğün mekanı, Fotoğrafçı, Gelinlik, Abiye, Kına, Nişan, Sünnet
        3. Bot Yanıtladı mı?: Evet/Hayır
        """
    
    # JSON kelimesini ekleyerek döndür
    return base_prompt + "\n\nLütfen yanıtınızı JSON formatında verin."

def analyze_message(message, message_type="user", retries=2):
    """Mesaj analizi için optimize edilmiş fonksiyon"""
    system_prompt = load_system_prompt()
    
    if message_type == "bot":
        system_prompt += "\n\nNOT: Bu bir bot yanıtıdır, analiz ederken buna göre değerlendirme yap."
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"JSON formatında yanıtla: {message}"}  # JSON kelimesi eklendi
                ],
                temperature=0.2,
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
                if all(key in result for key in ["sentiment", "topic", "bot_answered"]):
                    return result
                raise ValueError("Eksik alanlar var")
            except json.JSONDecodeError:
                cleaned = content.strip().replace("```json", "").replace("```", "")
                return json.loads(cleaned)
                
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < retries - 1:
                time.sleep(API_DELAY * (attempt + 0.5))
            continue
    
    return {
        "sentiment": "Nötr",
        "topic": "Diğer",
        "bot_answered": "Hayır" if message_type == "user" else "Evet"
    }

def process_all_messages():
    """Tüm mesajları toplu halde işler"""
    print("🔍 Tüm mesajlar işleniyor...")
    
    try:
        # Kullanıcı mesajlarını yükle
        with open('/Users/Hp/Desktop/Vivollo_project/data/raw_chats.txt', 'r', encoding='utf-8') as f:
            user_messages = [line.strip() for line in f if line.strip()]
        
        # Bot yanıtlarını yükle
        with open('/Users/Hp/Desktop/Vivollo_project/data/bot_responses.txt', 'r', encoding='utf-8') as f:
            bot_messages = [line.strip() for line in f if line.strip()]
        
        print(f"📊 {len(user_messages)} kullanıcı mesajı ve {len(bot_messages)} bot mesajı bulundu")
        
        # Mesajları birleştir ve tip bilgisi ekle
        all_messages = (
            [{"text": msg, "type": "user"} for msg in user_messages] +
            [{"text": msg, "type": "bot"} for msg in bot_messages]
        )
        
        results = []
        total_count = len(all_messages)
        success_count = 0
        
        for i, msg in enumerate(all_messages, 1):
            try:
                if i % 20 == 0:
                    print(f"⏳ İşleniyor: {i}/{total_count} (Başarı: {success_count}/{i-1})")
                
                prediction = analyze_message(msg["text"], msg["type"])
                results.append({
                    "message": msg["text"],
                    "message_type": msg["type"],
                    "llm_prediction": prediction
                })
                success_count += 1
                
                # Her 50 mesajda bir ara kayıt
                if i % 50 == 0:
                    save_results(results)
                    time.sleep(API_DELAY)
                    
            except Exception as e:
                print(f"❌ Mesaj {i} işlenirken hata: {str(e)}")
                continue
        
        save_results(results)
        print(f"\n✅ Tamamlandı! Başarılı işlem: {success_count}/{total_count}")
        
    except Exception as e:
        print(f"❌ Dosya okuma hatası: {e}")

def save_results(results):
    """Sonuçları dosyaya kaydeder"""
    try:
        output_path = '/Users/Hp/Desktop/Vivollo_project/data/llm_outputs.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"💾 Sonuçlar kaydedildi: {output_path}")
    except Exception as e:
        print(f"❌ Kayıt hatası: {e}")

if __name__ == "__main__":
    start_time = time.time()
    process_all_messages()
    print(f"⏱️ Toplam süre: {time.time()-start_time:.2f} saniye")

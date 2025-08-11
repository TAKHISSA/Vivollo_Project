import pandas as pd
import re
from pathlib import Path
from io import StringIO  # Bu satırı ekliyoruz

def temizle_ve_kaydet(kaynak_dosya, hedef_dosya="/Users/Hp/Desktop/Vivollo_project/data/100temiz.csv"):
    """
    CSV dosyasını temizleyip yeni bir dosyaya kaydeder.
    
    Args:
        kaynak_dosya (str): Temizlenecek CSV dosya yolu
        hedef_dosya (str): Temizlenmiş verinin kaydedileceği dosya (varsayılan: 100temiz.csv)
    """
    try:
        # Dosyayı ham olarak oku
        with open(kaynak_dosya, 'r', encoding='utf-8') as f:
            ham_icerik = f.read()
        
        # 1. Tırnak temizleme
        icerik = re.sub(r'"{2,3}(.*?)"{2,3}', r'"\1"', ham_icerik)
        
        # 2. Markdown/HTML temizleme
        icerik = re.sub(r'\*\*(.*?)\*\*', r'\1', icerik)
        icerik = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', icerik)
        
        # 3. Özel karakter temizleme
        icerik = re.sub(r'[\r\t]+', '', icerik)
        
        # 4. Pandas ile okuma
        df = pd.read_csv(
            StringIO(icerik),
            sep=';',
            quotechar='"',
            engine='python',
            on_bad_lines='warn'
        )
        
    except Exception as e:
        print(f"⚠️ Okuma hatası: {str(e)} - Alternatif yöntem deniyorum...")
        # Alternatif okuma yöntemi
        df = pd.read_csv(
            kaynak_dosya,
            sep=';',
            quotechar='"',
            engine='python',
            on_bad_lines='skip',
            encoding='utf-8'
        )
        
        # Manuel temizlik
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(r'"{2,3}', '"', regex=True)
                df[col] = df[col].str.replace(r'\*\*|\]\(.*?\)|\[', '', regex=True)
    
    # 5. Son temizlik
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(r'^"|"$', '', regex=True)
            df[col] = df[col].str.strip()
    
    # 6. Kaydetmeden önce kontrol
    print("\nÖrnek Temizlenmiş Veri:")
    print(df.head(3).to_markdown())
    
    # 7. Kaydetme
    kaydetme_yolu = Path(kaynak_dosya).parent / hedef_dosya
    df.to_csv(kaydetme_yolu, index=False, sep=';', encoding='utf-8', quoting=csv.QUOTE_MINIMAL)
    print(f"\n✅ Temizlenmiş veri kaydedildi: {kaydetme_yolu}")

# Gerekli importlar
import csv

# Kullanım
if __name__ == "__main__":
    temizle_ve_kaydet(
        kaynak_dosya='/Users/Hp/Desktop/Vivollo_project/data/manual_labels3.csv',
        hedef_dosya='/Users/Hp/Desktop/Vivollo_project/data/100temiz.csv'
    )

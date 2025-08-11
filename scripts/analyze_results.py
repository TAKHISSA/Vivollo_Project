import json
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import re

# Metin normalleştirme: tırnak, boşluk, satır sonu farklarını temizle
def normalize_text(s):
    return re.sub(r'\s+', ' ', str(s).strip().strip('"').strip()).strip()

def load_data():
    # LLM çıktıları
    with open('/Users/Hp/Desktop/Vivollo_project/data/llm_outputs.json', 'r', encoding='utf-8') as f:
        llm_data = json.load(f)

    # Manuel etiketler
    manual_data = pd.read_csv(
        '/Users/Hp/Desktop/Vivollo_project/data/manual_labels.csv',
        encoding='utf-8',
        sep=';',
        quotechar='"',
        on_bad_lines='warn'
    )

    # Fazladan tırnak ve boşluk temizleme
    manual_data = manual_data.applymap(lambda x: normalize_text(x))

    return llm_data, manual_data

def generate_report(llm_data, manual_data):
    results = []
    for manual_row in manual_data.itertuples():
        msg_norm = normalize_text(manual_row.message)
        llm_row = next((x for x in llm_data if normalize_text(x['message']) == msg_norm), None)
        
        if llm_row:
            results.append({
                "message": manual_row.message,
                "sentiment_manual": manual_row.sentiment,
                "sentiment_llm": llm_row['llm_prediction']['sentiment'],
                "topic_manual": manual_row.topic,
                "topic_llm": llm_row['llm_prediction']['topic'],
                "bot_manual": manual_row.bot_answered,
                "bot_llm": llm_row['llm_prediction']['bot_answered']
            })
    df = pd.DataFrame(results)
    return df

def analyze_results(df):
    if df.empty:
        raise ValueError("⚠️ comparison_df boş! Eşleşme bulunamadı. Mesaj formatlarını kontrol et.")
    
    metrics = {}
    for col in ['sentiment', 'topic', 'bot']:
        metrics[col] = {
            'accuracy': accuracy_score(df[f'{col}_manual'], df[f'{col}_llm']),
            'correct': int((df[f'{col}_manual'] == df[f'{col}_llm']).sum()),
            'total': len(df),
            'report': classification_report(df[f'{col}_manual'], df[f'{col}_llm'], output_dict=True, zero_division=0)
        }
    return metrics

if __name__ == "__main__":
    # Verileri yükle
    llm_data, manual_data = load_data()

    # Rapor verisi üret
    comparison_df = generate_report(llm_data, manual_data)

    # Eşleşmeyen mesajlar
    matched_messages = set(comparison_df['message']) if not comparison_df.empty else set()
    unmatched = [msg for msg in manual_data['message'] if msg not in matched_messages]
    print(f"⚠️ Eşleşmeyen {len(unmatched)} mesaj bulundu (örnekler):", unmatched[:5])

    # Doğruluk analizi
    accuracy_results = analyze_results(comparison_df)

    # Markdown rapor
    report = """# Doğruluk Raporu\n\n| Metric | Doğru | Toplam | Doğruluk |\n|--------|-------|--------|----------|\n"""
    for metric, vals in accuracy_results.items():
        report += f"| {metric.capitalize()} | {vals['correct']} | {vals['total']} | {vals['accuracy']:.2%} |\n"
    
    report += "\n## Detaylı Metrikler\n
python\n"
    for metric in accuracy_results:
        report += f"{metric}:\n{pd.DataFrame(accuracy_results[metric]['report']).to_markdown()}\n\n"
    report += "
"
    
    # Kaydet
    with open('/Users/Hp/Desktop/Vivollo_project/accuracy_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Rapor oluşturuldu! Toplam {len(comparison_df)} eşleşen mesaj analiz edildi.")

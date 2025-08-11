import csv
from pathlib import Path

def quote_csv_values(input_path, output_path):
    """CSV dosyasındaki tüm değerleri tırnak içine alır, orijinal yapıyı korur"""
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.reader(infile, delimiter=';')
            writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_ALL)
            
            for row in reader:
                # Her bir değeri tırnak içine al
                quoted_row = [f'"{value}"' for value in row]
                writer.writerow(quoted_row)
                
        print(f"✅ İşlem tamamlandı. Çıktı: {output_path}")
    
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Dosya yolları
    input_csv = Path('/Users/Hp/Desktop/Vivollo_project/data/manual_labels.csv')
    output_csv = Path('/Users/Hp/Desktop/Vivollo_project/data/manual_labels_quoted.csv')
    
    # İşlemi gerçekleştir
    quote_csv_values(input_csv, output_csv)
    
    # Önizleme yapalım
    print("\nİlk 5 satır önizleme:")
    with open(output_csv, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 5:
                print(line.strip())
            else:
                break

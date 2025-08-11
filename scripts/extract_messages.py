import json

def extract_messages():
    with open('/Users/Hp/Desktop/Vivollo_project/data/conversation.json', 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    user_messages = []
    bot_responses = []
    
    for conv in conversations:
        for msg in conv['messages']:
            # Kullanıcı mesajlarını al (sender_id null veya bot değilse ve internal değilse)
            if (msg['sender_id'] is None or msg['sender_id'] != 'bf17272dc3f0') and not msg['is_internal'] and msg['type'] in ['TEXT', 'SELECTED_OPTION']:
                if 'text' in msg['content']:
                    user_messages.append(msg['content']['text'])
            
            # Bot yanıtlarını da kaydet (analiz için)
            if msg['sender_id'] == 'bf17272dc3f0' and not msg['is_internal'] and msg['type'] == 'TEXT':
                if 'text' in msg['content']:
                    bot_responses.append(msg['content']['text'])
    
    # raw_chats.txt'ye yaz
    with open('/Users/Hp/Desktop/Vivollo_project/data/raw_chats.txt', 'w', encoding='utf-8') as f:
        for msg in user_messages:
            f.write(f"{msg}\n")
    
    # Bot yanıtlarını da kaydet (manuel etiketleme için)
    with open('/Users/Hp/Desktop/Vivollo_project/data/bot_responses.txt', 'w', encoding='utf-8') as f:
        for resp in bot_responses:
            f.write(f"{resp}\n")

if __name__ == "__main__":
    extract_messages()

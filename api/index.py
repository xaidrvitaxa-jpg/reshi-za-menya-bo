import json
import os
import random
import requests
from http.server import BaseHTTPRequestHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                
                if text == '/start':
                    reply = "Привет! 👋\nЯ бот «Реши за меня».\nНапиши варианты через запятую, например:\nпаста, пицца, суши, салат"
                elif text == '/help':
                    reply = "Просто напиши варианты выбора."
                else:
                    options = [x.strip() for x in text.replace('\n', ',').split(',') if x.strip()]
                    if len(options) > 1:
                        choice = random.choice(options)
                        reply = f"🎲 Я выбираю:\n**{choice}**"
                    else:
                        reply = "Напиши хотя бы 2 варианта через запятую."
                
                send_message(chat_id, reply)
        except Exception as e:
            print("Error:", e)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

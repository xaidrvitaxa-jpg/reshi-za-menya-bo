import json
import os
import random
from http.server import BaseHTTPRequestHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_message(chat_id, text):
    # Пока просто заглушка — позже сделаем нормальную отправку
    print(f"Отправляем в чат {chat_id}: {text}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data)
        
        try:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                reply = "Привет! Я бот «Реши за меня». Напиши варианты через запятую, и я выберу один."
            elif text == '/help':
                reply = "Просто напиши варианты: паста, пицца, суши"
            else:
                options = [x.strip() for x in text.split(',') if x.strip()]
                if options:
                    choice = random.choice(options)
                    reply = f"Я выбираю: **{choice}** 🎲"
                else:
                    reply = "Напиши варианты через запятую"
            
            send_message(chat_id, reply)
        except:
            pass  # если ошибка — игнорируем
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

from http.server import BaseHTTPRequestHandler
import json
import os
import random
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_message(chat_id, text):
    if not TOKEN:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length'))
            data = json.loads(self.rfile.read(length))
            if 'message' in data:
                msg = data['message']
                chat_id = msg['chat']['id']
                text = msg.get('text', '')

                if text == '/start':
                    reply = "Привет! Бот работает! Напиши варианты."
                else:
                    reply = "Бот на месте. Пока тестируем."

                send_message(chat_id, reply)
        except:
            pass

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

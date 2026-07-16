import json
import os
import random
import requests

def send_message(chat_id, text):
    token = os.environ.get("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def handler(request):
    try:
        if request.method == "POST":
            update = json.loads(request.body)
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")

                if text == "/start":
                    reply = "Привет! 👋 Напиши варианты через запятую."
                else:
                    options = [x.strip() for x in text.replace("\n", ",").split(",") if x.strip()]
                    if len(options) > 1:
                        choice = random.choice(options)
                        reply = f"🎲 Я выбираю:\n**{choice}**"
                    else:
                        reply = "Напиши варианты через запятую, например:\nпаста, пицца, суши"

                send_message(chat_id, reply)
    except Exception as e:
        print("Error:", str(e))
    
    return {
        "statusCode": 200,
        "body": "ok"
    }

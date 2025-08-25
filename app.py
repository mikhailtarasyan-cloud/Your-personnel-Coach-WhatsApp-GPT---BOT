import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# Init Flask
app = Flask(__name__)

# Init OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загружаем системный промт из файла
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")

    if not incoming_msg:
        resp = MessagingResponse()
        resp.message("Écris-moi quelque chose pour commencer 💪")
        return str(resp)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ],
            temperature=0.9,
            max_tokens=600
        )
        gpt_response = completion.choices[0].message.content.strip()
    except Exception as e:
        gpt_response = f"Erreur avec l'IA : {e}"

    resp = MessagingResponse()
    resp.message(gpt_response)
    return str(resp)

@app.route("/", methods=["GET"])
def index():
    return "✅ Bot WhatsApp '100% CASH' est en ligne."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


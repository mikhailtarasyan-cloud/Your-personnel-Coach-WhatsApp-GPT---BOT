from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Берём ключи из Environment Variables
# openai.api_key больше не нужен для новой версии

# Добавляем маршрут для главной страницы
@app.route("/")
def home():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        return f"""
        <h1>🤖 WhatsApp GPT Bot</h1>
        <p>✅ Сервер работает!</p>
        <p>✅ OpenAI API ключ загружен: {api_key[:10]}...</p>
        <p>📱 WhatsApp endpoint: <a href="/whatsapp">/whatsapp</a></p>
        <p>🧪 Тест: curl -X POST /whatsapp -d "Body=Привет"</p>
        """
    else:
        return f"""
        <h1>🤖 WhatsApp GPT Bot</h1>
        <p>❌ OpenAI API ключ не настроен!</p>
        <p>Проверьте файл .env</p>
        """

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        resp = MessagingResponse()
        msg = resp.message()

        if incoming_msg:
            # Проверяем API ключ
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "Error: OPENAI_API_KEY not set", 500
            
            # Проверяем, что ключ не пустой
            if api_key == "your_openai_api_key_here":
                return "Error: Please set your actual OpenAI API key in .env file", 500
            
            print(f"API Key loaded: {api_key[:10]}...")  # Отладочная информация
            
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            reply = response.choices[0].message.content
            msg.body(reply)
        return str(resp)
    except Exception as e:
        print(f"Error in whatsapp_reply: {str(e)}")  # Отладочная информация
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Проверяем переменные окружения при запуске
    api_key = os.getenv("OPENAI_API_KEY")
    print("=" * 50)
    print("🚀 Запуск WhatsApp GPT Bot")
    print("=" * 50)
    
    if api_key and api_key != "your_openai_api_key_here":
        print(f"✅ OpenAI API ключ загружен: {api_key[:10]}...")
    else:
        print("❌ OpenAI API ключ НЕ загружен!")
        print("Проверьте файл .env")
    
    print(f"🌐 Сервер запускается на порту 5005")
    print(f"📱 WhatsApp endpoint: http://localhost:5005/whatsapp")
    print(f"🏠 Главная страница: http://localhost:5005/")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=5005, debug=True)

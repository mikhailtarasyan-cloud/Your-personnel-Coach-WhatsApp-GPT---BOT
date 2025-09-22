"""
Исправленная версия AI-Наставника с улучшенной обработкой ошибок
"""
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
import pickle
from datetime import datetime
from dotenv import load_dotenv
import traceback

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Простая версия без сложных импортов для начала
def get_simple_response(message, phone_number):
    """Простая функция ответа для тестирования"""
    try:
        # Импортируем OpenAI только когда нужно
        import openai
        
        # Проверяем API ключ
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            return "❌ OpenAI API ключ не настроен. Проверьте файл .env"
        
        # Создаем клиента
        client = openai.OpenAI(api_key=api_key)
        
        # Простой системный промпт
        system_prompt = """Вы — AI-наставник по продуктивности. Отвечайте кратко и по делу. 
        Помогайте пользователям с планированием, мотивацией и достижением целей.
        Автор программы: Михаил Тарасьян - менеджер, инвестор, коуч, спортсмен."""
        
        # Создаем сообщения
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Получаем ответ от AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Ошибка AI: {e}")
        return f"Извините, произошла ошибка: {str(e)}"

# Главная страница
@app.route("/")
def home():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return """
        <h1>🎯 AI-Наставник по продуктивности</h1>
        <p>❌ OpenAI API ключ не настроен!</p>
        <p>Проверьте файл .env</p>
        """
    
    return f"""
    <h1>�� AI-Наставник по продуктивности</h1>
    <h2>Программа "Верни контроль: Решительность и дисциплина"</h2>
    <p>✅ Сервер работает!</p>
    <p>✅ OpenAI API ключ загружен: {api_key[:10]}...</p>
    <p>�� WhatsApp endpoint: <a href="/whatsapp">/whatsapp</a></p>
    <p>�� Тест: curl -X POST /whatsapp -d "Body=Привет, я готов начать"</p>
    <hr>
    <h3>�� Возможности:</h3>
    <ul>
        <li><strong>AI-коучинг:</strong> персональные рекомендации</li>
        <li><strong>Мотивация:</strong> поддержка и вдохновение</li>
        <li><strong>Планирование:</strong> помощь с целями и задачами</li>
    </ul>
    <h3>��‍💼 Об авторе:</h3>
    <p><strong>Михаил Тарасьян</strong> - менеджер, инвестор, коуч, спортсмен. 
    Создатель программы "Верни контроль: Решительность и дисциплина" для развития 
    личной эффективности и достижения целей.</p>
    """

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        print("=== WHATSAPP REQUEST ===")
        print(f"Headers: {dict(request.headers)}")
        print(f"Form data: {dict(request.form)}")
        print(f"Values: {dict(request.values)}")
        
        incoming_msg = request.values.get("Body", "").strip()
        phone_number = request.values.get("From", "unknown")
        
        print(f"Message: '{incoming_msg}'")
        print(f"Phone: {phone_number}")
        
        resp = MessagingResponse()
        msg = resp.message()
        
        if not incoming_msg:
            msg.body("Привет! Я получил пустое сообщение. Как дела?")
            return str(resp)
        
        # Проверяем API ключ
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            msg.body("❌ Сервер не настроен. Обратитесь к администратору.")
            return str(resp)
        
        # Получаем ответ от AI
        reply = get_simple_response(incoming_msg, phone_number)
        
        print(f"AI Response: {reply}")
        msg.body(reply)
        
        return str(resp)
        
    except Exception as e:
        print(f"Error in whatsapp_reply: {str(e)}")
        traceback.print_exc()
        
        # Возвращаем простой ответ даже при ошибке
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(f"Извините, произошла ошибка: {str(e)}")
        return str(resp)

# API для проверки статуса
@app.route("/status", methods=["GET"])
def status():
    api_key = os.getenv("OPENAI_API_KEY")
    return jsonify({
        "status": "ok" if api_key and api_key != "your_openai_api_key_here" else "error",
        "api_key_configured": bool(api_key and api_key != "your_openai_api_key_here"),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Запуск AI-Наставника (исправленная версия)")
    print("📚 Программа: Верни контроль: Решительность и дисциплина")
    print("��‍�� Автор: Михаил Тарасьян - менеджер, инвестор, коуч, спортсмен")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print(f"✅ OpenAI API ключ загружен: {api_key[:10]}...")
    else:
        print("❌ OpenAI API ключ НЕ загружен!")
        print("Проверьте файл .env")
    
    print("🌐 Сервер запускается на порту 5005")
    print("📱 WhatsApp endpoint: http://localhost:5005/whatsapp")
    print("🏠 Главная страница: http://localhost:5005/")
    print("🧪 Тест: curl -X POST /whatsapp -d \"Body=Привет, я готов начать\"")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5005, debug=True)

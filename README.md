# 🤖 WhatsApp GPT Bot

Интеллектуальный WhatsApp бот на базе OpenAI GPT, развёрнутый через Render + Twilio Sandbox.

## ✨ Возможности

- 💬 **Автоматические ответы** на сообщения в WhatsApp
- 🧠 **Искусственный интеллект** на базе GPT-4o-mini
- 🌐 **Веб-интерфейс** для обработки webhook'ов
- 🚀 **Готов к развертыванию** на Render, Heroku и других платформах

## 🛠️ Технологии

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4o-mini API
- **WhatsApp**: Twilio API
- **Deployment**: Render, Heroku
- **WSGI Server**: Gunicorn

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/your-username/whatsapp-gpt-bot-2.git
   cd whatsapp-gpt-bot-2
   ```

2. **Создайте виртуальное окружение**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

5. **Запустите приложение**
   ```bash
   python app.py
   ```

Приложение будет доступно по адресу: http://localhost:5001

## 🌐 Развертывание

### Render

1. Создайте новый Web Service на Render
2. Подключите ваш GitHub репозиторий
3. Добавьте переменную окружения `OPENAI_API_KEY`
4. Укажите команду запуска: `gunicorn app:app`
5. Deploy!

### Heroku

1. Создайте приложение на Heroku
2. Подключите репозиторий
3. Добавьте переменную окружения `OPENAI_API_KEY`
4. Deploy!

## 🔧 Настройка Twilio

1. Зарегистрируйтесь на [Twilio](https://www.twilio.com/)
2. Перейдите в WhatsApp Sandbox
3. Настройте webhook URL: `https://your-app.onrender.com/whatsapp`
4. Следуйте инструкциям для подключения WhatsApp

## 📁 Структура проекта

```
whatsapp-gpt-bot-2/
├── app.py                 # Основное Flask приложение
├── requirements.txt       # Python зависимости
├── Procfile              # Конфигурация для Heroku
├── .gitignore            # Исключения для Git
├── README.md             # Документация
├── activate.sh           # Скрипт активации виртуального окружения
└── RUN_INSTRUCTIONS.md   # Подробные инструкции по запуску
```

## 🔑 Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|--------------|
| `OPENAI_API_KEY` | API ключ OpenAI | ✅ |

## 📡 API Endpoints

### POST /whatsapp
Обрабатывает входящие WhatsApp сообщения через Twilio webhook.

**Параметры:**
- `Body` - текст сообщения от пользователя

**Ответ:**
- TwiML ответ для Twilio

## 🧪 Тестирование

### Тест API endpoint
```bash
curl -X POST http://localhost:5001/whatsapp \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Привет, как дела?"
```

### Тест в браузере
Откройте http://localhost:5001 в браузере

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🆘 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте [Issues](https://github.com/your-username/whatsapp-gpt-bot-2/issues)
2. Создайте новый Issue с описанием проблемы
3. Опишите шаги для воспроизведения ошибки

## 🙏 Благодарности

- [OpenAI](https://openai.com/) за GPT API
- [Twilio](https://www.twilio.com/) за WhatsApp интеграцию
- [Flask](https://flask.palletsprojects.com/) за веб-фреймворк

---

⭐ Если проект вам понравился, поставьте звездочку!

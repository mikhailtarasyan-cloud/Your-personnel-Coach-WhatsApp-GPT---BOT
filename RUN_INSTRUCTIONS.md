# Инструкции по запуску WhatsApp GPT Bot

## 🚀 Быстрый запуск

### 1. Активация виртуального окружения
```bash
# Способ 1: Через скрипт
./activate.sh

# Способ 2: Вручную
source venv/bin/activate
```

### 2. Установка переменной окружения
```bash
export OPENAI_API_KEY="ваш_ключ_openai_здесь"
```

### 3. Запуск приложения
```bash
python app.py
```

Приложение будет доступно по адресу: http://localhost:5001

## 📋 Что установлено

- ✅ **Flask 3.1.2** - веб-фреймворк
- ✅ **Twilio 9.7.2** - для WhatsApp интеграции
- ✅ **OpenAI 1.102.0** - для GPT API
- ✅ **Gunicorn 23.0.0** - WSGI сервер для продакшена

## 🔧 Тестирование

### Локальное тестирование
1. Запустите приложение: `python app.py`
2. Откройте браузер: http://localhost:5001
3. Протестируйте endpoint: http://localhost:5001/whatsapp

### Тестирование через curl
```bash
curl -X POST http://localhost:5001/whatsapp \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Привет, как дела?"
```

## ⚠️ Важные замечания

1. **API ключ OpenAI обязателен** для работы с GPT
2. **Twilio Sandbox** нужен для полноценного тестирования WhatsApp
3. **ngrok** может понадобиться для тестирования webhook'ов

## 🆘 Устранение проблем

### Ошибка "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY="ваш_ключ"
```

### Ошибка импорта модулей
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Порт 5000 занят
Измените порт в `app.py` или остановите другие приложения на этом порту.

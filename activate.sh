#!/bin/bash
# Скрипт для активации виртуального окружения
echo "Активация виртуального окружения..."
source venv/bin/activate
echo "Виртуальное окружение активировано!"
echo "Теперь вы можете запустить проект командой: python app.py"
echo ""
echo "Не забудьте установить переменную окружения OPENAI_API_KEY:"
echo "export OPENAI_API_KEY='ваш_ключ_openai_здесь'"



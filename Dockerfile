FROM python:3.11-slim

# Установка зависимостей
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все исходники
COPY . .


# Порт, на котором будет работать сервер
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

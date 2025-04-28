# Используем базовый образ Python, указанный вами.
FROM python:3.11-slim

# Устанавливаем переменные окружения для оптимизации Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Устанавливаем пакеты, необходимые для сборки зависимостей Python
# (например, psycopg2 требует libpq-dev) и клиента PostgreSQL.
# Очищаем кэш apt после установки для уменьшения размера образа.
RUN apt update && apt install -y --no-install-recommends postgresql-client build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера.
WORKDIR /app

# Копируем файл зависимостей раньше остального кода для лучшего кэширования Docker.
COPY mysite/requirements.txt .

# Обновляем pip и устанавливаем зависимости из requirements.txt.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта в рабочую директорию.
# Убедитесь, что структура папок верна (mysite/requirements.txt, mysite/ и т.д.).
COPY mysite/ .

# (Опционально) Если вы собираете статические файлы в образ
# Убедитесь, что STATIC_ROOT настроен в settings.py
# RUN python manage.py collectstatic --noinput

# Информируем Docker, что контейнер слушает на порту 8000.
EXPOSE 8000

# Эта команда CMD будет ПЕРЕОПРЕДЕЛЕНА директивой 'command' в docker-compose.yml,
# если 'command' там присутствует. Если вы удалите 'command' из docker-compose.yml,
# то выполнится эта команда.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
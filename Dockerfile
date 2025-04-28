FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update && apt install -y --no-install-recommends postgresql-client build-essential libpq-dev && rm -rf /var/lib/apt/lists*

WORKDIR /app

COPY mysite/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY mysite/ .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
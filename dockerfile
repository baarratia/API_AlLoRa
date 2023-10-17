FROM python:3.8

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/api_allora

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
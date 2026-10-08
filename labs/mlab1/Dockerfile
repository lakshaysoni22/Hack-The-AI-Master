FROM python:3.9-slim

WORKDIR /app

RUN pip install flask sqlite3

COPY app.py /app/app.py

EXPOSE 5000

CMD ["python", "app.py"]

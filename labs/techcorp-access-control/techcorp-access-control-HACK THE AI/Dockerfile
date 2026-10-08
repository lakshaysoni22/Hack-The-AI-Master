FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Bind only to localhost of the container by default; when mapping ports
# with `-p 127.0.0.1:5000:5000` on the host, the app remains local-only.
ENV FLASK_APP=app.py

EXPOSE 5000

RUN python3 -c "from app import init_db; init_db()"

CMD ["python3", "app.py"]

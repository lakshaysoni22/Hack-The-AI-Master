FROM python:3.9-slim

WORKDIR /app

COPY crypto_challenge.py /app/crypto_challenge.py

EXPOSE 9999

# We'll use socat to expose the python script over a TCP port, 
# or just run a simple python socket server. Let's use python socket server inside the script.
CMD ["python", "crypto_challenge.py"]

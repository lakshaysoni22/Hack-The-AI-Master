#!/bin/bash

if [ "$1" == "--docker" ]; then
    echo "Starting HACK THE AI Platform via Docker Compose..."
    docker-compose up --build
else
    echo "Installing requirements..."
    pip install -r requirements.txt
    
    echo "Starting HACK THE AI Platform..."
    python app.py
fi

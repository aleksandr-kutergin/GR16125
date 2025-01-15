#!/bin/bash

echo "Stopping and removing containers..."
docker-compose down

echo "Building and starting containers..."
docker-compose up --build
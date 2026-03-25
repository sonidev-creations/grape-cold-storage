# Grape Cold Storage Monitoring System

## Description
This project monitors a grape cold storage using ESP32, DHT22, MQ-3 gas sensor, and an LCD.  
It displays readings in real-time on a web dashboard using Flask and Firebase Realtime Database.

## Components
- ESP32 Dev Module
- DHT22 Temperature & Humidity Sensor
- MQ-3 Gas Sensor
- 16x2 I2C LCD
- Python Flask backend
- Firebase Realtime Database
- Simple frontend (HTML + JS)

## Setup Instructions

### 1. ESP32
- Open `GrapeColdStorage.ino` in Arduino IDE.
- Replace WiFi credentials and Flask server IP.
- Upload to ESP32.

### 2. Backend
- Navigate to `backend/`.
- Install dependencies:

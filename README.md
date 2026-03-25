<img src="https://raw.githubusercontent.com/sonidev-creations/grape-cold-storage/main/assets/screenshot.png" width="700"/>
# 🍇 Smart Grape Cold Storage Monitoring System using IoT

Smart Grape Cold Storage Monitoring System is an IoT-based solution that monitors temperature, humidity, and gas levels in real-time to maintain optimal storage conditions and prevent spoilage.

---

## 🚀 Features

- 📡 Real-time monitoring of temperature, humidity, and gas levels  
- 🚨 Instant SMS alerts using Twilio when limits are exceeded  
- ☁️ Cloud data storage using Firebase  
- 📊 Live data visualization through web dashboard  
- 🔄 Continuous updates from ESP32 sensors  
- 🔐 Secure handling of API keys using environment variables  

---

## 🛠️ Tech Stack

- **Hardware:** ESP32, DHT22, MQ3 Sensors  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** Firebase Realtime Database  
- **Alerts:** Twilio SMS API  

---

## 📁 Project Structure

```
grape-cold-storage/
├── assets/
│   └── screenshot.png
├── arduino/
│   └── esp32_grape_monitoring.ino
├── backend/
│   ├── app.py
│   ├── alert_service.py
│   ├── firebase_config.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── static/
│   └── script.js
├── esp32_studio.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ How It Works

1. ESP32 collects sensor data (temperature, humidity, gas)  
2. Data is sent to the Flask backend via API  
3. Backend stores data in Firebase  
4. If values exceed safe limits, an SMS alert is triggered  
5. Data is displayed on the web dashboard in real-time  

---

## ▶️ Running Locally

1. Clone the repository:
```bash
git clone https://github.com/sonidev-creations/grape-cold-storage.git
cd grape-cold-storage
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your credentials:
```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
FIREBASE_API_KEY=your_key
```

5. Run the application:
```bash
python backend/app.py
```

Open in browser: http://127.0.0.1:5000

---

## 👨‍💻 Developer

Made with ❤️ by **Soni P**  
📧 iamsoni.btech@gmail.com  
🔗 https://www.linkedin.com/in/sonipandian/

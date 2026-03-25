import os
from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
ALERT_TO_NUMBER    = os.getenv("ALERT_TO_NUMBER")

TEMP_MAX  = 8.0
TEMP_MIN  = 0.0
HUMID_MAX = 90.0
HUMID_MIN = 30.0

_last_alert = {}
ALERT_COOLDOWN_MINUTES = 30


def _cooldown_ok(key):
    last = _last_alert.get(key)
    if not last:
        return True
    return (datetime.now() - last).total_seconds() / 60 >= ALERT_COOLDOWN_MINUTES


def send_sms(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=ALERT_TO_NUMBER
        )

        print("✅ SMS Sent:", msg.sid)
        return {"success": True, "sid": msg.sid}

    except Exception as e:
        print("❌ SMS Failed:", e)
        return {"success": False, "error": str(e)}


def check_and_alert(data):
    results = []

    temp = data.get("temperature")
    hum  = data.get("humidity")
    time = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    if temp is not None and temp > TEMP_MAX and _cooldown_ok("temp_high"):
        msg = (
            f"⚠️ எச்சரிக்கை!\n"
            f"🍇 திராட்சை குளிர்சாதனத்தில் வெப்பநிலை அதிகமாக உள்ளது.\n"
            f"தற்போது: {temp}°C\n"
            f"அளவு: {TEMP_MAX}°C\n"
            f"நேரம்: {time}\n"
            f"👉 உடனே குளிர்சாதனத்தை சரிபார்க்கவும்!"
        )
        res = send_sms(msg)
        if res["success"]:
            _last_alert["temp_high"] = datetime.now()
        results.append({"type": "temp_high", **res})

    if temp is not None and temp < TEMP_MIN and _cooldown_ok("temp_low"):
        msg = (
            f"⚠️ எச்சரிக்கை!\n"
            f"🍇 வெப்பநிலை மிகவும் குறைந்துள்ளது.\n"
            f"தற்போது: {temp}°C\n"
            f"👉 திராட்சை உறையக்கூடும்!\n"
            f"உடனே சரிசெய்யவும்."
        )
        res = send_sms(msg)
        if res["success"]:
            _last_alert["temp_low"] = datetime.now()
        results.append({"type": "temp_low", **res})

    if hum is not None and hum > HUMID_MAX and _cooldown_ok("hum_high"):
        msg = (
            f"⚠️ எச்சரிக்கை!\n"
            f"🍇 ஈரப்பதம் அதிகமாக உள்ளது.\n"
            f"தற்போது: {hum}%\n"
            f"👉 பூஞ்சை / பழுதடைதல் அபாயம்!\n"
            f"காற்றோட்டத்தை சரிபார்க்கவும்."
        )
        res = send_sms(msg)
        if res["success"]:
            _last_alert["hum_high"] = datetime.now()
        results.append({"type": "hum_high", **res})

    if hum is not None and hum < HUMID_MIN and _cooldown_ok("hum_low"):
        msg = (
            f"⚠️ எச்சரிக்கை!\n"
            f"🍇 ஈரப்பதம் குறைவாக உள்ளது.\n"
            f"தற்போது: {hum}%\n"
            f"👉 திராட்சை உலரக்கூடும்!\n"
            f"உடனே சரிசெய்யவும்."
        )
        res = send_sms(msg)
        if res["success"]:
            _last_alert["hum_low"] = datetime.now()
        results.append({"type": "hum_low", **res})

    return results

if __name__ == "__main__":
    test = {
        "temperature": 12,
        "humidity": 20,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print("Testing alerts...")
    print(check_and_alert(test))
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <DHT.h>

#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>  // For I2C LCD

#define WIFI_SSID "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define API_KEY "YOUR_API_KEY"
#define DATABASE_URL "YOUR_DATABASE_URL"

FirebaseData fbdo;
FirebaseConfig config;
FirebaseAuth auth;

#define DHTPIN 4
#define DHTTYPE DHT22
#define GASPIN 34

#define RED_LED 2
#define GREEN_LED 15

#define GAS_THRESHOLD 2000
#define TEMP_THRESHOLD 35

DHT dht(DHTPIN, DHTTYPE);

hd44780_I2Cexp lcd;

void setup() {

  Serial.begin(115200);

  lcd.begin(16, 2);
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int t = 0;
  while (WiFi.status() != WL_CONNECTED && t < 20) {
    delay(500);
    lcd.print(".");
    t++;
  }
  lcd.clear();
  lcd.print(WiFi.status() == WL_CONNECTED ? "WiFi OK" : "WiFi Fail");

  pinMode(GASPIN, INPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  dht.begin();

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  auth.user.email = "esp32@test.com";
  auth.user.password = "12345678";

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gasRaw = analogRead(GASPIN);
  int gasVal = gasRaw / 0.82;

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Sensor Error");
    delay(3000);
    return;
  }

  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print(" H:");
  lcd.print(hum, 0);
  lcd.print("   ");

  lcd.setCursor(0, 1);
  if (gasVal > GAS_THRESHOLD || temp > TEMP_THRESHOLD) {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    lcd.print("ALERT       ");
  } else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    lcd.print("NORMAL      ");
  }

  Serial.print("Temp:");
  Serial.print(temp);
  Serial.print(" Hum:");
  Serial.print(hum);
  Serial.print(" Gas:");
  Serial.println(gasVal);

  if (Firebase.ready()) {
    Firebase.RTDB.setFloat(&fbdo, "/grape-data/temperature", temp);
    Firebase.RTDB.setFloat(&fbdo, "/grape-data/humidity", hum);
    Firebase.RTDB.setInt(&fbdo, "/grape-data/gas", gasVal);
  }

  delay(4000);
}
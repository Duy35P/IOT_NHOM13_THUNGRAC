#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// --- CẤU HÌNH WIFI & MQTT ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

// Đổi topic theo cấu trúc quản lý nhiều thùng rác (bin1, bin2,...)
const char* topic_khoangcach = "doan/nhom15/bin1/khoangcach";
const char* topic_canhbao = "doan/nhom15/bin1/canhbao";
const char* topic_gps = "doan/nhom15/bin1/gps";
const char* topic_battery = "doan/nhom15/bin1/battery";
const char* topic_config = "doan/nhom15/bin1/config"; // Topic nhận cấu hình từ Web
const char* topic_lock = "doan/nhom15/bin1/lock";   // Node-RED Rule 1: "1" = khóa nắp (chống tràn), "0" = mở khóa
const char* topic_mode = "doan/nhom15/bin1/mode";   // Node-RED Rule 2: "ECO" = đo 30s/lần, "NORMAL" = 3s/lần
bool lid_locked = false;
bool eco_mode = false;
unsigned long lastDeniedMsg = 0;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastDistanceMsg = 0;
unsigned long lastAlertMsg = 0;
unsigned long lastReconnectAttempt = 0;

// --- PINOUT ---
#define TRIG_PIN 5
#define ECHO_PIN 18
#define SERVO_PIN 13
#define PIR_PIN 19
#define BUZZER_PIN 12
#define LED_RED 14
#define LED_GREEN 27
#define GPS_BTN 4

// --- HẰNG SỐ & BIẾN TOÀN CỤC ---
int distance_threshold = 5; // Ngưỡng đầy mặc định (có thể đổi từ Web)
int battery_level = 85;     // Giả lập lượng pin còn lại (85%)
#define OPEN_ANGLE 90         
#define CLOSE_ANGLE 0         
#define OPEN_TIME 3000        

Servo lidServo;

// Hàm callback nhận lệnh từ Web (để đổi ngưỡng)
void callback(char* topic, byte* payload, unsigned int length) {
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)payload[i];
  }
  
  if (String(topic) == topic_config) {
    Serial.print("Nhan duoc lenh thay doi nguong rac: ");
    Serial.println(messageTemp);
    int new_threshold = messageTemp.toInt();
    if (new_threshold > 0 && new_threshold <= 100) {
      distance_threshold = new_threshold;
      Serial.print("=> Da cap nhat nguong moi: ");
      Serial.println(distance_threshold);
    }
  } else if (String(topic) == topic_lock) {
    lid_locked = (messageTemp == "1");
    Serial.println(lid_locked ? "=> Node-RED: KHOA NAP (chong tran)" : "=> Node-RED: MO KHOA NAP");
  } else if (String(topic) == topic_mode) {
    eco_mode = (messageTemp == "ECO");
    Serial.println(eco_mode ? "=> Node-RED: che do ECO (30s)" : "=> Node-RED: che do NORMAL (3s)");
  }
}

void setup_wifi() {
  Serial.print("Dang ket noi WiFi...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
  } else {
    Serial.println("\nWiFi Failed!");
  }
}

boolean reconnect() {
  // ponytail: guard wifi before mqtt connect to survive network drops
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Mat WiFi, dang ket noi lai...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 10) {
      delay(300);
      Serial.print(".");
      attempts++;
    }
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println(" That bai!");
      return false;
    }
    Serial.println(" WiFi OK!");
  }

  Serial.print("Ket noi MQTT Broker...");
  String clientId = "ESP32_ThungRac_15_bin1_";
  clientId += String(random(0xffff), HEX);
  if (client.connect(clientId.c_str())) {
    Serial.println("Thanh cong!");
    // Đăng ký nhận lệnh cấu hình từ Web khi vừa kết nối xong
    client.subscribe(topic_config);
    client.subscribe(topic_lock);
    client.subscribe(topic_mode);
    return true;
  }
  Serial.println("That bai!");
  return false;
}

void setup() {
  Serial.begin(9600);
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(GPS_BTN, INPUT_PULLUP); 
  
  ESP32PWM::allocateTimer(1);
  lidServo.setPeriodHertz(50);
  lidServo.attach(SERVO_PIN, 500, 2400);
  lidServo.write(CLOSE_ANGLE); 
  
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED, LOW);
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback); // Khởi tạo callback để nhận lệnh
  
  Serial.println("HE THONG SMART TRASH BIN 1 - KHOI DONG XONG");
}

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return round(duration * 0.034 / 2);
}

void loop() {
  if (!client.connected()) {
    long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      if (reconnect()) {
        lastReconnectAttempt = 0;
      }
    }
  } else {
    client.loop();
  }

  // TÍNH NĂNG 1: KIỂM TRA RÁC ĐẦY DỰA TRÊN NGƯỠNG MỚI
  long distance = getDistance();
  if (distance > 0 && distance <= distance_threshold) {
    tone(BUZZER_PIN, 1000); 
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    
    if (client.connected() && millis() - lastAlertMsg > 5000) {
      client.publish(topic_canhbao, "⚠️ KHẨN CẤP: THÙNG RÁC 1 ĐÃ ĐẦY!");
      Serial.print("! CANH BAO ! - Khoang cach: ");
      Serial.println(distance);
      lastAlertMsg = millis();
    }
  } else {
    noTone(BUZZER_PIN);     
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, HIGH);
  }
  
  // Gửi khoảng cách & Pin lên mạng định kỳ
  if (client.connected() && millis() - lastDistanceMsg > (eco_mode ? 30000UL : 3000UL)) {
      char msg[10];
      dtostrf(distance, 1, 2, msg);
      client.publish(topic_khoangcach, msg);
      
      char batMsg[10];
      itoa(battery_level, batMsg, 10);
      client.publish(topic_battery, batMsg);
      
      lastDistanceMsg = millis();
  }
  
  // TÍNH NĂNG 2: MỞ NẮP TỰ ĐỘNG
  int pirState = digitalRead(PIR_PIN);
  if (pirState == HIGH && lid_locked) {
    if (client.connected() && millis() - lastDeniedMsg > 5000) {
      client.publish(topic_canhbao, "Thùng đang khóa (đầy) - từ chối người dùng");
      lastDeniedMsg = millis();
    }
  } else if (pirState == HIGH) { 
    Serial.println("=> Phat hien nguoi! Dang mo nap...");
    if(client.connected()) client.publish(topic_canhbao, "Có người đến gần! Đang mở nắp...");
    lidServo.write(OPEN_ANGLE);  
    delay(OPEN_TIME);            
    lidServo.write(CLOSE_ANGLE); 
    Serial.println("=> Da dong nap.");
    if(client.connected()) client.publish(topic_canhbao, "Đã đóng nắp.");
    
    while (digitalRead(PIR_PIN) == HIGH) {
      delay(100);
    }
  }
  
  // TÍNH NĂNG 3: NÚT BẤM GPS
  if (digitalRead(GPS_BTN) == LOW) {
    delay(500); // Debounce
    Serial.println("[GPS] Toa do hien tai: Lat: 10.8037, Lng: 106.6294");
    if(client.connected()) {
      client.publish(topic_gps, "Lat: 10.8037, Lng: 106.6294");
    }
  }
  
  delay(100); 
}

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <XPT2046_Touchscreen.h>
#include <WiFi.h>
#include "time.h"

// ===== WIFI =====
const char* ssid = "";
const char* password = "";

// ===== NTP =====
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -21600;
const int daylightOffset_sec = 0;

// ===== VARIABLES CALCULADORA =====
float num1 = 0;
float num2 = 0;
char operacion = '+';
float resultado = 0;

// ===== TFT =====
#define TFT_CS 5
#define TFT_DC 2
#define TFT_RST 4
Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_RST);

// ===== TOUCH =====
#define TOUCH_CS 17
XPT2046_Touchscreen ts(TOUCH_CS);

String texto = "";
int con = 0;
bool activoCaja = false;

// Coordenadas caja de texto
int cajaX = 40, cajaY = 60, cajaW = 240, cajaH = 40;

// Coordenadas botón
int btnX = 100, btnY = 140, btnW = 120, btnH = 40;

// ===== CALIBRACIÓN =====
int MIN_X = 200, MAX_X = 3800;
int MIN_Y = 200, MAX_Y = 3800;

// ===== CONTROL =====
int pantallaActual = 0;
int xStart = 0;
int xEnd = 0;
bool tocando = false;

// ===== ENCENDIDO =====
bool pantallaEncendida = true;
unsigned long tiempoToque = 0;
bool presionando = false;

// ===== REFRESCO =====
unsigned long ultimoRefresh = 0;

// ===== BOTONES =====
void dibujarBoton(int x, int y, int w, int h, String texto, uint16_t color) {
  tft.fillRoundRect(x, y, w, h, 10, color);
  tft.drawRoundRect(x, y, w, h, 10, ILI9341_WHITE);

  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(2);

  int tx = x + (w / 2) - (texto.length() * 6);
  int ty = y + (h / 2) - 8;

  tft.setCursor(tx, ty);
  tft.print(texto);
}

void efectoBoton(int x, int y, int w, int h) {
  tft.drawRoundRect(x, y, w, h, 10, ILI9341_YELLOW);
  delay(80);
}

// ===== FECHA =====
String obtenerFecha() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) return "Sin fecha";
  char buffer[30];
  strftime(buffer, sizeof(buffer), "%d/%m/%Y", &timeinfo);
  return String(buffer);
}

// ===== SETUP =====
void setup() {
  Serial.begin(115200);

  tft.begin();
  tft.setRotation(1);
  dibujarUI();
  ts.begin();
  ts.setRotation(2);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  dibujarPantalla();
}

// ===== LOOP =====
void loop() {

  // actualizar fecha
  if (pantallaActual == 0 && millis() - ultimoRefresh > 1000) {
    pantallaInicio();
    ultimoRefresh = millis();
  }

  // encendido
  if (ts.touched()) {
    if (!presionando) {
      tiempoToque = millis();
      presionando = true;
    }
  } else if (presionando) {
    if (millis() - tiempoToque > 800) {
      pantallaEncendida = !pantallaEncendida;
      if (pantallaEncendida) dibujarPantalla();
      else tft.fillScreen(ILI9341_BLACK);
    }
    presionando = false;
  }

  if (!pantallaEncendida) return;

  // ===== TOUCH =====
  if (ts.touched()) {
    delay(120);
    TS_Point p = ts.getPoint();
    int x = map(p.x, MIN_X, MAX_X, 0, 320);
    int y = map(p.y, MIN_Y, MAX_Y, 0, 240);
    // 👇 AQUÍ VA
    Serial.print("X: ");
    Serial.print(x);
    Serial.print(" Y: ");
    Serial.println(y);

    // detectar inicio swipe
    if (!tocando) {
      xStart = x;
      tocando = true;
    }

    // ===== APPS =====
  
  if (pantallaActual == 2) {
    // CALCULADORA (área más amplia y precisa)
    if (x >= 30 && x <= 110 && y >= 70 && y <= 150) {
      efectoBoton(40, 80, 60, 60);
      pantallaActual = 3;
      dibujarPantalla();
      delay(200); // evita doble toque
    }
    // AJUSTES
    else if (x >= 130 && x <= 210 && y >= 70 && y <= 150) {
      efectoBoton(140, 80, 60, 60);
      pantallaActual = 4;
      dibujarPantalla();
      delay(200);
    }
}

    // ===== CALCULADORA =====
    if (pantallaActual == 3) {

      if (x > 10 && x < 90 && y > 10 && y < 50) {
        efectoBoton(10,10,80,40);
        pantallaActual = 2;
        dibujarPantalla();
      }

      if (x > 40 && x < 140 && y > 70 && y < 110) {
        num1++;
        pantallaCalculadora();
      }

      if (x > 180 && x < 280 && y > 70 && y < 110) {
        num2++;
        pantallaCalculadora();
      }

      if (x > 40 && x < 90 && y > 130 && y < 170) operacion = '+';
      if (x > 100 && x < 150 && y > 130 && y < 170) operacion = '-';
      if (x > 160 && x < 210 && y > 130 && y < 170) operacion = '*';
      if (x > 220 && x < 270 && y > 130 && y < 170) operacion = '/';

      if (x > 80 && x < 240 && y > 180 && y < 220) {
        efectoBoton(80,180,160,40);

        if (operacion == '+') resultado = num1 + num2;
        if (operacion == '-') resultado = num1 - num2;
        if (operacion == '*') resultado = num1 * num2;
        if (operacion == '/' && num2 != 0) resultado = num1 / num2;

        pantallaCalculadora();
      }
    } 
    if (pantallaActual == 4) {

      int x = map(p.x, 200, 3800, 0, 320);
      int y = map(p.y, 200, 3800, 0, 240);

      Serial.print("X: "); Serial.print(x);
      Serial.print(" Y: "); Serial.println(y);
      
      if (x > 10 && x < 90 && y > 10 && y < 50) {
        efectoBoton(10,10,80,40);
        pantallaActual = 2;
        dibujarPantalla();
      }

     // Detectar toque en caja de texto
      if (x > cajaX && x < cajaX + cajaW &&
        y > cajaY && y < cajaY + cajaH) {
        activoCaja = true;
        Serial.println("Caja activada");
     }

      // Detectar botón
      if (x > btnX && x < btnX + btnW &&
        y > btnY && y < btnY + btnH) {
        Serial.println("Botón presionado");
        con++;
        if(con == 1)
        {  
          texto = "El salvador";
          actualizarTexto();
        }
        else if(con == 2)
        {  
          texto = "Guatemala";
          actualizarTexto();
        }
        else if(con == 3)
        {  
          texto = "Honduras";
          actualizarTexto();
        }
        else if(con == 4)
        {  
          texto = "Nicaragua";
          actualizarTexto();
        }
        else if(con == 5)
        {  
          texto = "Costa rica";
          actualizarTexto();
          con = -5;
        }
     }

    }

  } else if (tocando) {

    // detectar final del swipe
    TS_Point p2 = ts.getPoint();
    int xFinal = map(p2.x, MIN_X, MAX_X, 0, 320);

    int diferencia = xFinal - xStart;

    if (diferencia > 50 && pantallaActual > 0) {
      pantallaActual--;
      dibujarPantalla();
    }

    if (diferencia < -50 && pantallaActual < 2) {
      pantallaActual++;
      dibujarPantalla();
    }

    tocando = false;
  }
}

// ===== PANTALLAS =====
void dibujarPantalla() {

  if (pantallaActual == 0) fondoInicio();
  if (pantallaActual == 1) fondoUsuario();
  if (pantallaActual == 2) fondoHola();
  if (pantallaActual == 3) fondoHola();
  if (pantallaActual == 4) fondoHola();

  if (pantallaActual == 0) pantallaInicio();
  if (pantallaActual == 1) pantallaNombre();
  if (pantallaActual == 2) pantallaApps();
  if (pantallaActual == 3) pantallaCalculadora();
  if (pantallaActual == 4) dibujarUI();
  
  for (int i = 0; i < 3; i++) {
    int color = (i == pantallaActual) ? ILI9341_WHITE : ILI9341_DARKGREY;
    tft.fillCircle(130 + i * 20, 220, 5, color);
  }
}

// ===== UI =====
void dibujarIcono(int x, int y, String nombre, uint16_t color) {
  tft.fillRoundRect(x, y, 60, 60, 15, color);

  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(3);
  tft.setCursor(x + 22, y + 18);
  tft.print("+");

  tft.setTextSize(2);
  tft.setCursor(x + 5, y + 70);
  tft.print(nombre);
  
}

void dibujarIcon2(int x, int y, String nombre, uint16_t color) {
  tft.fillRoundRect(x, y, 60, 60, 15, color);

  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(3);
  tft.setCursor(x + 22, y + 18);
  tft.print("A");

  tft.setTextSize(2);
  tft.setCursor(x + 5, y + 70);
  tft.print(nombre);
  
}

void pantallaInicio() {
  tft.fillRect(0, 0, 320, 200, ILI9341_BLACK);

  tft.setTextColor(ILI9341_CYAN);
  tft.setTextSize(3);
  tft.setCursor(40, 30);
  tft.print("INICIO");

  tft.setTextColor(ILI9341_CYAN);
  tft.setTextSize(3);
  tft.setCursor(40, 70);
  tft.print(texto);

  tft.setTextSize(2);
  tft.setCursor(40, 130);
  tft.print(obtenerFecha());
}

void pantallaNombre() {
  tft.fillScreen(ILI9341_BLACK);

  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(3);
  tft.setCursor(40, 40);
  tft.print("USUARIO");

  tft.setTextSize(2);
  tft.setCursor(40, 120);
  tft.print("Mauricio");
}

void pantallaApps() {
  tft.fillScreen(ILI9341_BLACK);

  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(3);
  tft.setCursor(100, 20);
  tft.print("APPS");

  dibujarIcono(40, 80, "Calc", ILI9341_BLUE);
  dibujarIcon2(140, 80, "Ajust", ILI9341_GREEN);
  dibujarIcono(240, 80, "App3", ILI9341_RED);
}

void pantallaCalculadora() {
  tft.fillScreen(ILI9341_BLACK);

  tft.setTextColor(ILI9341_CYAN);
  tft.setTextSize(3);
  tft.setCursor(110, 10);
  tft.print("CALC");

  dibujarBoton(10, 10, 80, 40, "BACK", ILI9341_RED);

  tft.drawRect(40, 70, 100, 40, ILI9341_WHITE);
  tft.setCursor(60, 85);
  tft.setTextSize(2);
  tft.print(num1);

  tft.drawRect(180, 70, 100, 40, ILI9341_WHITE);
  tft.setCursor(200, 85);
  tft.print(num2);

  dibujarBoton(80, 180, 160, 40, "CALC", ILI9341_GREEN);

  tft.setTextColor(ILI9341_YELLOW);
  tft.setCursor(60, 230);
  tft.print("R: ");
  tft.print(resultado);
}

void dibujarUI() {
  // Caja de texto
  tft.drawRect(cajaX, cajaY, cajaW, cajaH, ILI9341_WHITE);
  dibujarBoton(10, 10, 80, 40, "BACK", ILI9341_RED);
  // Botón
  tft.fillRect(btnX, btnY, btnW, btnH, ILI9341_BLUE);
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(btnX + 25, btnY + 12);
  tft.print("Enviar");
}

// ===== ACTUALIZAR TEXTO =====
void actualizarTexto() {
  tft.fillRect(cajaX + 2, cajaY + 2, cajaW - 4, cajaH - 4, ILI9341_BLACK);
  tft.setCursor(cajaX + 5, cajaY + 12);
  tft.setTextColor(ILI9341_GREEN);
  tft.print(texto);
}

// ===== FONDOS =====
void fondoInicio() {
  for (int y = 0; y < 240; y++) {
    uint16_t color = tft.color565(0, y, 255);
    tft.drawFastHLine(0, y, 320, color);
  }
}

void fondoUsuario() {
  tft.fillScreen(tft.color565(0, 150, 80));
}

void fondoHola() {
  tft.fillScreen(ILI9341_BLACK);
}

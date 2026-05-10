#include <Wire.h>
#include "MAX30105.h"

MAX30105 particleSensor;

void setup() {
  // Mantenemos 115200 para que el buffer de Python no se llene de basura,
  // pero controlaremos la frecuencia de envío con delay.
  Serial.begin(115200);

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("Error_Sensor");
    while (1);
  }

  // Configuración de "baja velocidad" para el sensor
  byte ledBrightness = 60;
  byte sampleAverage = 4; 
  byte ledMode = 2; 
  int sampleRate = 50;   // Bajamos a 50Hz (mínimo para que sea estable)
  int pulseWidth = 411; 
  int adcRange = 4096;

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
}

void loop() {
  long irValue = particleSensor.getIR();
  long redValue = particleSensor.getRed();

  // Enviamos solo si hay un dedo cerca para no mandar basura a la IA
  if (irValue > 50000) {
    // Formato simple: Rojo,IR
    Serial.print(redValue);
    Serial.print(",");
    Serial.println(irValue);
  }

  // Delay de 20ms = ~50 lecturas por segundo (perfecto para procesar en Python)
  delay(20); 
}
# 🕹️ Arcade Console

<div align="center">

  <p><b>Ein Retro-Arcade-Konzept für den Raspberry Pi Pico 2W mit MicroPython.</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/MicroPython-2B303B?style=flat-square&logo=micropython&logoColor=white" alt="MicroPython">
    <img src="https://img.shields.io/badge/Hardware-Raspberry_Pi_Pico_2W-C51A4A?style=flat-square&logo=raspberrypi&logoColor=white" alt="Hardware">
    <img src="https://img.shields.io/badge/Status-Ausbildungsprojekt-orange?style=flat-square" alt="Status">
  </p>
</div>

---

## 📖 Über das Projekt
**Arcade Console** ist ein eingebettetes MicroPython-Projekt für den **Raspberry Pi Pico 2W**, das im Rahmen meiner Umschulung zum **Fachinformatiker für Systemintegration** entstanden ist. Ziel war es, eine performante 128x64 OLED-Ausgabe mit einer robusten Hardware-Eingabe (Joysticks) und modularer Spielelogik zu verbinden.

---

## 🎯 Ziel des Projekts
Der Schwerpunkt lag auf einer stabilen und sauberen Umsetzung von:
* ⚙️ **Hardware-Integration:** Robuste Joystick-Verarbeitung (Kalibrierung, Deadzone, Hysterese) und I2C-Ansteuerung des SSD1306-Displays.
* 🧩 **Modulare Architektur:** Klare Trennung von Hardware, Engine, UI und Spielmodi.
* 🕹️ **1D-Bedienkonzept:** Flüssige Menü-Navigation und optimierte Spielmodi für analoge Achsen und Taster.

> *Das Projekt diente primär Lern- und Demonstrationszwecken im Bereich Embedded Python.*

---

## 🛠️ Verwendete Technologien
| Bereich | Technologie / Tool |
| :--- | :--- |
| **Mikrocontroller** | Raspberry Pi Pico 2W |
| **Sprache** | MicroPython |
| **Display** | SSD1306 OLED (128x64) |
| **Eingabe** | 2x 1-Achsen-Joysticks mit Tastern |

---

## 📌 Hinweis
Dieses Repository dokumentiert ein Ausbildungsschulprojekt und zeigt den erreichten Entwicklungsstand sowie die umgesetzten Hardware- und Software-Konzepte. Es erhebt keinen Anspruch auf Vollständigkeit.

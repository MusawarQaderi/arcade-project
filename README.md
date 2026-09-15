# Arcade Console

Retro-Arcade-Konzept für den **Raspberry Pi Pico 2W** mit **MicroPython**, **SSD1306 OLED (128x64)** und **zwei 1-Achsen-Joysticks mit Tastern**.

---

## Projektkontext

Dieses Projekt ist – ähnlich wie mein **FootballHub-Projekt** – im Rahmen meiner **Fachinformatiker-Umschulung** während der **Python-Projektphase** entstanden.  
Ziel war es, ein strukturiertes Embedded-/MicroPython-Projekt mit klarer Input-Architektur, performanter 128x64-Ausgabe und modularer Spielelogik umzusetzen.

---

## Projektziel

Der Fokus liegt auf einer stabilen, klaren und bewusst reduzierten Arcade-Umgebung für 1D-Eingaben:

- saubere Trennung von Hardware, Engine, UI und Spielmodi
- robuste Joystick-Verarbeitung (Kalibrierung, Deadzone, Hysterese)
- konsistente Darstellung auf dem SSD1306-Display
- wartbare, erweiterbare Projektstruktur

---

## Hardware-Setup (Projektbasis)

| Funktion         | Pico-Pin      | Hinweis                            |
|------------------|---------------|------------------------------------|
| Joystick 1 VRy   | GP26 / ADC0   | einzelne Analogachse               |
| Joystick 1 SW    | GP14          | `Pin.PULL_UP`, gedrückt = Low      |
| Joystick 2 VRy   | GP27 / ADC1   | einzelne Analogachse               |
| Joystick 2 SW    | GP15          | `Pin.PULL_UP`, gedrückt = Low      |
| OLED SDA         | GP0           | I2C-Datenleitung                   |
| OLED SCL         | GP1           | I2C-Taktleitung                    |

---

## Technische Merkmale

### Input-Verarbeitung
- Boot-Kalibrierung beider Analogachsen
- sichtbarer Kalibrierungsstatus beim Start
- Deadzone + Hysterese zur Stabilisierung der Neutralstellung
- Menü-Navigation mit Wiederholverhalten bei gehaltenem Input
- kurzer Tastendruck: **SELECT**
- langer Tastendruck: **BACK**
- Achsinvertierung pro Spieler konfigurierbar

### UI/Rendering (128x64)
- 8-Pixel-Zeilenraster für saubere Textausrichtung
- automatische Kürzung langer Labels mit `...`
- zentrale Clipping-Logik im Renderer
- maximal ein `display.show()` pro Frame

### Intro-Sequenz
Originale Retro-Sequenz **„BLITZ ARCADE“** mit:
- Kalibrierungsbalken
- 1-Bit-Speedlines
- Frame/Ring-Animation
- Logo-Slide-in
- Shine-Effekt
- Skip per Button

---

## Spielmodi (1D-kompatibel)

- **Reflex Lane**  
  Ein-Spieler-Modus mit vertikaler Auswahlbewegung und Timing-Fokus.

- **Paddle Duel**  
  Zwei-Spieler-Paddle-Duell mit je einer vertikalen Achse pro Spieler.

- **Input Test**  
  Diagnoseansicht für beide Joysticks und Tasterzustände.

---

## Bewusste Abgrenzung

2D-lastige Modi wurden in diesem Projektstand gezielt entfernt bzw. deaktiviert, um ein konsistentes 1D-Eingabekonzept einzuhalten (z. B. Snake, Breakout, Tetris).

---

## Projektstruktur

```text
main.py
config.py
hardware.py
renderer.py
storage.py
engine/
  core.py
  input.py
  scenes.py
  timebase.py
ui/
  menu.py
games/
  reflex.py
  paddle_duel.py
docs/
  TESTING.md
```

---

## Kurzfazit

**Arcade Console** zeigt meinen praxisnahen Ansatz in der Umschulung:  
Hardware-nahe Python-Entwicklung, modulare Softwarestruktur und technische Reduktion auf ein klares, funktionales Bedienkonzept.

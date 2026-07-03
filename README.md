# Arcade Console

Retro arcade console for Raspberry Pi Pico 2W, MicroPython, SSD1306 OLED 128x64, and two one-axis joysticks with buttons.

## Important Pico install note

Copy the contents of this ZIP directly onto the Pico filesystem root. `main.py` and `config.py` must sit next to each other:

```text
/main.py
/config.py
/hardware.py
/renderer.py
/storage.py
/engine/...
/ui/...
/games/...
```

Do not copy only `main.py`. If `config.py` is missing from the same Pico folder, MicroPython will report `ImportError: no module named 'config'`.

`main.py` also adds its own folder to `sys.path` to make Thonny/subfolder execution more tolerant.

## Current focus

This refactor targets the strict Pico 2W wiring below and removes menu entries for games that require two-dimensional directional input. The UI is constrained to an 8-row grid because the SSD1306 built-in font is 8 px high.

## Hardware wiring

| Function | Pico pin | Notes |
|---|---:|---|
| Joystick 1 VRy | GP26 / ADC0 | single analog axis |
| Joystick 1 SW | GP14 | `Pin.PULL_UP`, pressed = low |
| Joystick 2 VRy | GP27 / ADC1 | single analog axis |
| Joystick 2 SW | GP15 | `Pin.PULL_UP`, pressed = low |
| OLED SDA | GP0 | kept compatible with existing repo config |
| OLED SCL | GP1 | kept compatible with existing repo config |

## Input behavior

- Boot-time center calibration averages both VRy axes before the intro starts.
- A calibration screen is shown so the boot does not look frozen.
- Deadzone and hysteresis prevent noisy neutral flicker.
- Menu UP/DOWN supports initial movement plus repeat while held.
- Short button press emits `SELECT`.
- Holding the button emits `BACK`.
- Per-player axis inversion flags are available in `config.py` and in the Settings menu.

## Startup intro

The boot now uses an original retro “BLITZ ARCADE” sequence:

- calibration progress bar
- fast one-bit speed lines
- expanding arcade frame/ring
- block-logo slide-in
- simple shine sweep
- skip with any button press

No third-party logo or trademark bitmap is copied.

## 128x64 UI rules

- Every text line is placed on an 8 px row.
- Long labels are clipped with ellipsis.
- The renderer owns clipping helpers.
- The app loop performs at most one `display.show()` per rendered frame.

## Kept 1D-compatible modes

- `Reflex Lane`: one-player lane-selection game using UP/DOWN + SELECT.
- `Paddle Duel`: two-player vertical paddle duel using one axis per player.
- `Input Test`: diagnostics for both joysticks.

## Removed / disabled 2D modes

The following modes are intentionally not shown because they normally require two-axis input or richer directional control:

- Snake
- Breakout
- Tetris
- Any optional 2D directional modes from the original architecture prompt

## Project structure

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

## Install

1. Flash MicroPython for Raspberry Pi Pico 2W.
2. Copy all files/folders from this ZIP to the Pico root.
3. Add the SSD1306 driver as `/ssd1306.py` if it is not already present.
4. Keep both joystick axes centered.
5. Reset the Pico.

Run manually if needed:

```python
import main
main.main()
```

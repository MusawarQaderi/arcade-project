## Summary

- Refactored input into a centralized `InputManager` for Pico 2W + MicroPython.
- Updated hardware mapping to the required one-axis joystick wiring:
  - P1 VRy GP26/ADC0, SW GP14/PULL_UP
  - P2 VRy GP27/ADC1, SW GP15/PULL_UP
- Added boot-time dynamic center calibration for both analog axes.
- Added a visible boot calibration screen so startup does not look frozen.
- Fixed Pico install/import robustness by documenting root-copy layout and adding a `sys.path` guard in `main.py`.
- Added deadzone, hysteresis, button debounce, menu repeat, and SELECT/BACK events per player.
- Reworked OLED UI around a strict 8-row 128x64 grid with text clipping/ellipsis.
- Replaced the basic intro with a short original retro `BLITZ ARCADE` intro:
  - speed lines
  - expanding frame/ring
  - block-logo slide-in
  - shine sweep
  - skip with any button
- Added a frame-limited scene loop with a single `display.show()` per rendered frame.
- Added multiplayer menu flow with separate P1/P2 focus indicators.
- Added 1D-compatible `Reflex Lane` and `Paddle Duel` modes.
- Added `docs/TESTING.md` with wiring and validation steps.

## Removed / disabled 2D modes

The following modes are not shown because they require two-axis or multidirectional input:

- Snake
- Breakout
- Tetris
- Optional 2D directional modes from the architecture prompt

## Test steps

1. Flash MicroPython to the Raspberry Pi Pico 2W.
2. Copy all files/folders from the ZIP to the Pico root so `/main.py` and `/config.py` are next to each other.
3. Copy `ssd1306.py` to the Pico filesystem if it is not already present.
4. Wire the OLED and joysticks exactly as documented in `docs/TESTING.md`.
5. Boot with both joystick axes released for center calibration.
6. Verify the calibration bar appears, then the `BLITZ` intro plays and can be skipped with any button.
7. Open `INPUT TEST` and verify P1/P2 axis direction, button debounce, SELECT, and BACK hold behavior.
8. Check all menu screens for text overlap on the 128x64 OLED.
9. Start `MULTIPLAYER -> PADDLE DUEL` and verify P1 controls the left paddle and P2 controls the right paddle.
10. Watch the intro and game animation for stable frame pacing and no repeated `show()` flicker.

# Arcade Console

Retro arcade console for Raspberry Pi Pico, MicroPython, SSD1306 OLED, dual analog joysticks, and two buttons.

## Status

This repository currently acts as the architecture and implementation foundation for a small open-source arcade console project. The goal is to evolve it into a modular, maintainable codebase with a clear engine/game separation, persistent storage, and room for multiple games and UI screens.

## Goals

- Modular engine with reusable input, rendering, menu, storage, and game-state layers
- Efficient OLED rendering for constrained hardware
- Easy addition of new games, menus, animations, and effects
- Persistent highscores, settings, achievements, and statistics
- Clean documentation and a professional project layout

## Suggested Project Structure

```text
ArcadeConsole/
	main.py
	config.py
	hardware.py
	renderer.py
	audio.py
	storage.py
	README.md
	requirements.md
	LICENSE
	engine/
	games/
	assets/
	fonts/
	effects/
	animations/
	ui/
	save/
	docs/
	tests/
```

## Architecture Outline

- `hardware`: display, input, I2C, and boot-time initialization
- `engine`: game loop, state management, rendering coordination, collision logic, and shared services
- `games`: one file per game, each built on the same engine contract
- `ui`: menus, overlays, dialogs, and HUD components
- `storage`: JSON-backed persistence for settings, scores, achievements, and statistics
- `assets`: sprites, icons, fonts, and animations

## Recommended Implementation Order

1. Define configuration and hardware abstraction
2. Implement the core engine loop and renderer
3. Build the menu system and persistent storage
4. Port existing games to the new architecture
5. Add achievements, statistics, and polish effects
6. Expand with additional games once the core is stable

## Coding Agent Prompt

See [PROMPT.md](PROMPT.md) for the refined implementation prompt that can be used for a coding agent.
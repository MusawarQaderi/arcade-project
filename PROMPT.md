# Coding Agent Prompt

You are an experienced embedded software developer and software architect.

I have an existing Arcade project for a Raspberry Pi Pico with an SSD1306 OLED 128x64 display, two analog joysticks, and two buttons. The current code may work, but it should be professionally restructured into a clean, modular, and extensible arcade console codebase.

## Primary Goal

Transform the project into a maintainable retro arcade console with a clear software architecture, efficient rendering, persistent storage, and a path for adding new games and features without turning the codebase into a monolith.

## Constraints

- Target hardware: Raspberry Pi Pico
- Runtime: MicroPython
- Display: SSD1306 OLED 128x64 over I2C
- Input: 2 analog joysticks, 2 buttons
- Priorities: low RAM usage, efficient display updates, stable frame pacing, minimal allocations

## Architecture Principles

- Separate hardware access, engine logic, UI, storage, and games
- Keep each module small and focused
- Avoid global state unless it is truly necessary
- Prefer reusable components over game-specific duplication
- Keep performance in mind at every layer
- Use clear names, small functions, and concise docstrings where they improve readability

## Suggested Project Layout

```text
ArcadeConsole/
  main.py
  config.py
  hardware.py
  renderer.py
  audio.py
  storage.py
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

## Core Engine Modules

- InputManager
- GameManager
- State or Scene Manager
- Renderer
- Sprite handling
- AnimationManager
- CollisionManager
- MenuManager
- StorageManager
- StatisticsManager
- AchievementManager
- Utility helpers

## Renderer Requirements

The renderer should be designed for constrained hardware and should support:

- text and centered text
- lines, rectangles, icons, and sprites
- menu rendering and HUD rendering
- selective or dirty updates where practical
- simple transitions such as blink, fade, shake, and scanlines
- effects that are optional if hardware cost is too high

## Menu and UI

Build a complete menu system with:

- main menu
- submenus
- settings
- highscores
- achievements
- statistics
- credits
- diagnostics or system information
- animated transitions and selection feedback

## Storage and Statistics

Persist settings, highscores, achievements, and gameplay statistics using a simple format such as JSON if it is suitable for MicroPython.

Track at least:

- total play time
- games started
- games finished
- wins and losses
- per-game highscore
- per-game playtime
- per-game statistics

## Games

Keep every game in its own file and make each game consume the same engine services. Existing games should be refactored rather than rewritten in a way that loses functionality.

Existing titles:

- Pong
- Snake
- Breakout
- Tetris

Optional later additions:

- Flappy Bird
- Space Invaders
- Asteroids
- Frogger
- Memory
- Simon Says
- Minesweeper
- Tron
- Doodle Jump
- simplified Pac-Man

## Quality Bar

- Keep functions small and testable
- Avoid magic numbers by using config values
- Add docstrings where they clarify behavior
- Use type hints where MicroPython supports them cleanly
- Avoid unnecessary abstraction if it hurts readability or performance
- Keep the implementation practical, not overengineered

## Documentation

When implementing the project, also maintain documentation for:

- hardware wiring and pinout
- project structure
- installation and startup
- how to add new games
- how to add new sprites or UI components
- architecture overview

## Working Style

1. Start with a short analysis of the current state.
2. Propose a target architecture.
3. Implement the smallest stable step first.
4. Verify the result before expanding scope.
5. If a feature is too heavy for the Pico, suggest a lighter alternative.

## Deliverables

- a clean and documented architecture
- a reusable engine foundation
- a modular game structure
- persistent settings, scores, and statistics
- a polished README that explains the project clearly
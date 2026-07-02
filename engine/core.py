"""Core application loop for the arcade console."""

import gc
import sys
import time

from engine.game_manager import GameManager
from engine.input import InputManager
from engine.state import AppState
from games import BreakoutGame, PongGame, SnakeGame, TetrisGame
from ui.menu import MenuManager


class ArcadeApp:
    """Owns the top-level flow of the arcade console."""

    def __init__(self, config, hardware, renderer, storage) -> None:
        self.config = config
        self.hardware = hardware
        self.renderer = renderer
        self.storage = storage
        self.input = InputManager(hardware)
        self.games = GameManager()
        self.breakout = BreakoutGame(config)
        self.pong = PongGame(config)
        self.snake = SnakeGame(config)
        self.tetris = TetrisGame(config)
        self.games.register(self.breakout.name, self.breakout)
        self.games.register(self.pong.name, self.pong)
        self.games.register(self.snake.name, self.snake)
        self.games.register(self.tetris.name, self.tetris)
        self.menu = MenuManager(renderer, self.games.names() + ["Highscores", "Settings", "Credits"], title="Main Menu")
        self.settings_menu = MenuManager(
            renderer,
            ["Display", "Sound", "Gameplay", "System Info", "Reset Highscores", "Back"],
            title="Settings",
        )
        self.pause_menu = MenuManager(renderer, ["Resume", "Restart", "Main Menu"], title="Paused")
        self.active_game = None
        self.active_game_name = None
        self.game_result_recorded = False
        self.running = False
        self.state = AppState.BOOT
        self.loaded_state = {}

    def run(self) -> None:
        self.running = True
        self.loaded_state = self.storage.load()
        self._show_boot_screen()
        self.state = AppState.MENU

        frame_delay = 1 / max(1, self.config.fps)
        while self.running:
            self.input.update()
            self._handle_input()
            self.renderer.clear()
            self._render_state()
            self.renderer.present()
            time.sleep(frame_delay)

        self.storage.save()

    def _show_boot_screen(self) -> None:
        stages = [
            "Initializing display",
            "Loading input",
            "Mounting save data",
            "Preparing games",
            "Ready",
        ]

        for stage_index, stage in enumerate(stages):
            self.renderer.clear()
            self._draw_intro_frame(stage_index)
            self._draw_intro_logo(stage_index)
            self._draw_scanlines(stage_index)
            self.renderer.draw_centered_text(stage, 45)
            if stage_index < len(stages) - 1:
                self.renderer.draw_centered_text("LOADING...", 55)
            elif stage_index % 2 == 0:
                self.renderer.draw_centered_text("PRESS ANY BUTTON", 55)

            progress_width = 78
            progress_x = 25
            progress_y = 55
            self.renderer.draw_box(progress_x, progress_y, progress_width, 6)
            filled_width = int((progress_width - 4) * (stage_index + 1) / len(stages))
            for line_y in range(progress_y + 1, progress_y + 5):
                if filled_width > 0:
                    self.renderer.draw_line(progress_x + 2, line_y, progress_x + 1 + filled_width, line_y)

            self.renderer.present()
            time.sleep(0.18)

        self.renderer.clear()
        self.renderer.draw_box(0, 0, self.config.width, self.config.height)
        self.renderer.draw_centered_text(self.config.app_name, 18)
        self.renderer.draw_centered_text("Press any button to begin", 34)
        self.renderer.draw_centered_text("Boot complete", 48)
        self.renderer.present()
        time.sleep(0.35)

    def _draw_intro_frame(self, stage_index: int) -> None:
        self.renderer.draw_box(0, 0, self.config.width, self.config.height)
        top_y = 8 + (stage_index % 2)
        bottom_y = self.config.height - 9 - (stage_index % 2)
        self.renderer.draw_line(5, top_y, self.config.width - 6, top_y)
        self.renderer.draw_line(5, bottom_y, self.config.width - 6, bottom_y)
        self.renderer.draw_line(5, top_y, 5, bottom_y)
        self.renderer.draw_line(self.config.width - 6, top_y, self.config.width - 6, bottom_y)

    def _draw_intro_logo(self, stage_index: int) -> None:
        blink = stage_index % 2 == 0
        self.renderer.draw_box(12, 17, 28, 20)
        self.renderer.draw_box(17, 21, 18, 12)
        self.renderer.draw_line(16, 35, 18, 38)
        self.renderer.draw_line(34, 35, 32, 38)
        self.renderer.draw_line(20, 23, 32, 23)
        self.renderer.draw_line(20, 30, 32, 30)
        if blink:
            self.renderer.draw_line(23, 24, 23, 29)
            self.renderer.draw_line(29, 24, 29, 29)

        self.renderer.draw_text("ARCADE", 46, 18)
        self.renderer.draw_text("CONSOLE", 46, 28)
        self.renderer.draw_text("RETRO", 46, 38)

    def _draw_scanlines(self, stage_index: int) -> None:
        offset = stage_index % 2
        for y in range(12 + offset, 53, 3):
            self.renderer.draw_line(7, y, self.config.width - 8, y)

    def _render_state(self) -> None:
        if self.state == AppState.MENU:
            self.renderer.draw_centered_text(self.config.app_name, 0)
            self.menu.render()
            return

        if self.state == AppState.PAUSED and self.active_game is not None:
            self.active_game.render(self.renderer)
            self._render_pause_overlay()
            return

        if self.state == AppState.SETTINGS:
            self.settings_menu.render()
            self.renderer.draw_text("Display", 72, 14)
            self.renderer.draw_text("Sound", 72, 24)
            self.renderer.draw_text("Gameplay", 72, 34)
            self.renderer.draw_text("Info", 72, 44)
            return

        if self.state == AppState.DISPLAY_SETTINGS:
            self._render_setting_page(
                "Display",
                [
                    "Brightness: %s" % self.storage.get_setting("brightness", 1),
                    "Resolution: %sx%s" % (self.config.width, self.config.height),
                    "Btn1: cycle",
                    "Btn2: back",
                ],
            )
            return

        if self.state == AppState.SOUND_SETTINGS:
            self._render_setting_page(
                "Sound",
                [
                    "Sound: %s" % self._on_off(self.storage.get_setting("sound", True)),
                    "Btn1: toggle",
                    "Btn2: back",
                ],
            )
            return

        if self.state == AppState.GAMEPLAY_SETTINGS:
            self._render_setting_page(
                "Gameplay",
                [
                    "Difficulty: %s" % self.storage.get_setting("difficulty", 1),
                    "Btn1: cycle",
                    "Btn2: back",
                ],
            )
            return

        if self.state == AppState.SYSTEM_INFO:
            free_memory = getattr(gc, "mem_free", lambda: 0)()
            platform_name = getattr(sys.implementation, "name", "python")
            self._render_setting_page(
                "System",
                [
                    "Platform: %s" % platform_name,
                    "FPS: %s" % self.config.fps,
                    "Free mem: %s" % free_memory,
                    "Save: %s" % self.config.storage_file,
                    "Btn2: back",
                ],
            )
            return

        if self.state == AppState.HIGHSCORES:
            self.renderer.draw_centered_text("Highscores", 0)
            self._render_highscores()
            self.renderer.draw_text("Btn2: Back", 0, 54)
            return

        if self.state == AppState.CREDITS:
            self.renderer.draw_centered_text("Credits", 0)
            self.renderer.draw_text("Arcade Console", 12, 18)
            self.renderer.draw_text("MicroPython on Pico", 12, 28)
            self.renderer.draw_text("Btn2: Back", 12, 48)
            return

        if self.active_game is not None:
            self.active_game.render(self.renderer)
            return

        self.renderer.draw_centered_text("Game state", 24)

    def _handle_input(self) -> None:
        if self.state == AppState.GAME and self.active_game is not None:
            self.active_game.update(self.input)
            if getattr(self.active_game, "game_over", False) and not self.game_result_recorded:
                self._record_game_result()
                self.state = AppState.GAME_OVER
            elif self.input.just_pressed("player2", "button"):
                self._open_pause_menu()
            return

        if self.state == AppState.PAUSED and self.active_game is not None:
            self._handle_pause_input()
            return

        if self.state == AppState.GAME_OVER and self.active_game is not None:
            if self.input.just_pressed("player1", "button"):
                self.active_game.reset()
                self.game_result_recorded = False
                self.state = AppState.GAME
            elif self.input.just_pressed("player2", "button"):
                self._exit_to_menu()
            return

        if self.state != AppState.MENU:
            if self.state == AppState.SETTINGS:
                self._handle_settings_input()
            elif self.state in (
                AppState.DISPLAY_SETTINGS,
                AppState.SOUND_SETTINGS,
                AppState.GAMEPLAY_SETTINGS,
                AppState.SYSTEM_INFO,
            ):
                self._handle_settings_subpage_input()
            elif self.state == AppState.HIGHSCORES or self.state == AppState.CREDITS:
                if self.input.just_pressed("player2", "button"):
                    self.state = AppState.MENU
            return

        if self.input.just_pressed("player1", "button"):
            selected = self.menu.selected()
            if selected == "Settings":
                self.state = AppState.SETTINGS
            elif selected == "Highscores":
                self.state = AppState.HIGHSCORES
            elif selected == "Credits":
                self.state = AppState.CREDITS
            else:
                self._start_game(selected)
            return

        if self.input.pressed("player1", "y"):
            self.menu.move_up()
        elif self.input.pressed("player1", "x"):
            self.menu.move_down()

    def _open_pause_menu(self) -> None:
        if self.active_game is None:
            return

        self.pause_menu.index = 0
        self.state = AppState.PAUSED

    def _handle_pause_input(self) -> None:
        if self.input.just_pressed("player2", "button"):
            self.state = AppState.GAME
            return

        if self.input.pressed("player1", "y"):
            self.pause_menu.move_up()
        elif self.input.pressed("player1", "x"):
            self.pause_menu.move_down()

        if not self.input.just_pressed("player1", "button"):
            return

        selected = self.pause_menu.selected()
        if selected == "Resume":
            self.state = AppState.GAME
        elif selected == "Restart":
            self._restart_active_game()
        elif selected == "Main Menu":
            self._exit_to_menu()

    def _handle_settings_input(self) -> None:
        if self.input.pressed("player1", "y"):
            self.settings_menu.move_up()
        elif self.input.pressed("player1", "x"):
            self.settings_menu.move_down()

        if not self.input.just_pressed("player1", "button"):
            return

        selected = self.settings_menu.selected()
        if selected == "Display":
            self.state = AppState.DISPLAY_SETTINGS
        elif selected == "Sound":
            self.state = AppState.SOUND_SETTINGS
        elif selected == "Gameplay":
            self.state = AppState.GAMEPLAY_SETTINGS
        elif selected == "System Info":
            self.state = AppState.SYSTEM_INFO
        elif selected == "Reset Highscores":
            self.storage.reset_highscores()
        elif selected == "Back":
            self.state = AppState.MENU

    def _handle_settings_subpage_input(self) -> None:
        if self.input.just_pressed("player2", "button"):
            self.state = AppState.SETTINGS
            return

        if self.state == AppState.DISPLAY_SETTINGS and self.input.just_pressed("player1", "button"):
            self.storage.cycle_setting("brightness", [1, 2, 3])
            return

        if self.state == AppState.SOUND_SETTINGS and self.input.just_pressed("player1", "button"):
            self.storage.toggle_setting("sound")
            return

        if self.state == AppState.GAMEPLAY_SETTINGS and self.input.just_pressed("player1", "button"):
            self.storage.cycle_setting("difficulty", [1, 2, 3])
            return

    def _render_setting_page(self, title, lines) -> None:
        self.renderer.draw_centered_text(title, 0)
        for index, line in enumerate(lines):
            self.renderer.draw_text(line, 8, 16 + index * 10)

    def _start_game(self, game_name) -> None:
        self.active_game = self.games.get(game_name)
        self.active_game_name = game_name
        self.game_result_recorded = False
        if self.active_game is not None:
            self.active_game.reset()
            self.storage.record_game_started()
            self.state = AppState.GAME

    def _restart_active_game(self) -> None:
        if self.active_game is None:
            return

        self.active_game.reset()
        self.game_result_recorded = False
        self.pause_menu.index = 0
        self.state = AppState.GAME

    def _exit_to_menu(self) -> None:
        self.active_game = None
        self.active_game_name = None
        self.game_result_recorded = False
        self.state = AppState.MENU

    def _record_game_result(self) -> None:
        if self.active_game is None or self.active_game_name is None:
            return

        score = self.active_game.get_score()
        self.storage.set_highscore(self.active_game_name, score)
        self.storage.record_game_finished()
        self.game_result_recorded = True
        self.storage.save()

    def _render_pause_overlay(self) -> None:
        self.renderer.draw_box(10, 8, 108, 48)
        self.renderer.draw_centered_text("PAUSED", 14)
        self.pause_menu.render()
        self.renderer.draw_text("Btn2: resume", 14, 50)

    def _render_highscores(self) -> None:
        self.renderer.draw_text("Breakout: %s" % self.storage.get_highscore("Breakout"), 12, 16)
        self.renderer.draw_text("Pong: %s" % self.storage.get_highscore("Pong"), 12, 26)
        self.renderer.draw_text("Snake: %s" % self.storage.get_highscore("Snake"), 12, 36)
        self.renderer.draw_text("Tetris: %s" % self.storage.get_highscore("Tetris"), 12, 46)

    def _on_off(self, value) -> str:
        return "On" if value else "Off"
        self.active_game = None
        self.active_game_name = None
        self.game_result_recorded = False
        self.state = AppState.MENU

    def _render_pause_overlay(self) -> None:
        self.renderer.draw_box(10, 8, 108, 48)
        self.renderer.draw_centered_text("PAUSED", 14)
        self.pause_menu.render()
        self.renderer.draw_text("Btn2: resume", 14, 50)

        score = self.active_game.get_score()
        self.storage.set_highscore(self.active_game_name, score)
        self.storage.record_game_finished()
        self.game_result_recorded = True
        self.storage.save()

    def _render_highscores(self) -> None:
        self.renderer.draw_text("Pong: %s" % self.storage.get_highscore("Pong"), 12, 16)
        self.renderer.draw_text("Snake: %s" % self.storage.get_highscore("Snake"), 12, 26)

    def _on_off(self, value) -> str:
        return "On" if value else "Off"
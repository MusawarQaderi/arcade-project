"""Tetris for the Pico arcade console."""

import random

from games.base import GameBase


class TetrisGame(GameBase):
    """Compact Tetris implementation for the shared engine."""

    name = "Tetris"

    SHAPES = [
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
    ]

    def __init__(self, config) -> None:
        self.config = config
        self.cell_size = 4
        self.top_offset = 10
        self.board_width = 10
        self.board_height = 13
        self.drop_interval = 8
        self.soft_drop_bonus = 1
        self.reset()

    def reset(self) -> None:
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.score = 0
        self.lines = 0
        self.game_over = False
        self.ticks = 0
        self.current_shape = None
        self.current_rotation = 0
        self.current_x = 0
        self.current_y = 0
        self._spawn_piece()

    def update(self, input_manager) -> None:
        if self.game_over:
            if input_manager.just_pressed("player1", "button"):
                self.reset()
            return

        if input_manager.just_pressed("player1", "button"):
            self._rotate_piece()

        axis_x = input_manager.current["player1"]["x"]
        axis_y = input_manager.current["player1"]["y"]

        if axis_x < 22000:
            self._move_piece(-1, 0)
        elif axis_x > 43000:
            self._move_piece(1, 0)

        self.ticks += 1
        if axis_y > 45000:
            self._soft_drop()
        elif self.ticks % self.drop_interval == 0:
            self._soft_drop()

    def render(self, renderer) -> None:
        renderer.draw_text("TETRIS", 0, 0)
        renderer.draw_text(str(self.score), 72, 0)

        for row_index in range(self.board_height):
            for column_index in range(self.board_width):
                if self.board[row_index][column_index]:
                    self._draw_cell(renderer, column_index, row_index)

        if self.current_shape is not None:
            for row_index, row in enumerate(self.current_shape[self.current_rotation]):
                for column_index, filled in enumerate(row):
                    if filled:
                        board_x = self.current_x + column_index
                        board_y = self.current_y + row_index
                        self._draw_cell(renderer, board_x, board_y)

        renderer.draw_box(0, self.top_offset, self.board_width * self.cell_size, self.board_height * self.cell_size)

        if self.game_over:
            renderer.draw_centered_text("Game Over", 22)
            renderer.draw_centered_text("Press A to restart", 34)

    def get_score(self) -> int:
        return self.score

    def _soft_drop(self) -> None:
        self._move_piece(0, 1)

    def _move_piece(self, delta_x: int, delta_y: int) -> bool:
        new_x = self.current_x + delta_x
        new_y = self.current_y + delta_y
        if self._collision(new_x, new_y, self.current_rotation):
            if delta_y > 0:
                self._lock_piece()
                self._clear_lines()
                self._spawn_piece()
            return False

        self.current_x = new_x
        self.current_y = new_y
        return True

    def _rotate_piece(self) -> None:
        next_rotation = (self.current_rotation + 1) % 4
        if not self._collision(self.current_x, self.current_y, next_rotation):
            self.current_rotation = next_rotation

    def _spawn_piece(self) -> None:
        self.current_shape = random.choice(self.SHAPES)
        self.current_rotation = 0
        self.current_x = (self.board_width - 4) // 2
        self.current_y = 0
        if self._collision(self.current_x, self.current_y, self.current_rotation):
            self.game_over = True

    def _lock_piece(self) -> None:
        for row_index, row in enumerate(self.current_shape[self.current_rotation]):
            for column_index, filled in enumerate(row):
                if not filled:
                    continue
                board_x = self.current_x + column_index
                board_y = self.current_y + row_index
                if 0 <= board_x < self.board_width and 0 <= board_y < self.board_height:
                    self.board[board_y][board_x] = 1

    def _clear_lines(self) -> None:
        remaining = []
        cleared = 0
        for row in self.board:
            if all(row):
                cleared += 1
            else:
                remaining.append(row)

        while len(remaining) < self.board_height:
            remaining.insert(0, [0 for _ in range(self.board_width)])

        self.board = remaining
        if cleared:
            self.lines += cleared
            self.score += cleared * 100

    def _collision(self, piece_x: int, piece_y: int, rotation: int) -> bool:
        shape = self.current_shape[rotation]
        for row_index, row in enumerate(shape):
            for column_index, filled in enumerate(row):
                if not filled:
                    continue
                board_x = piece_x + column_index
                board_y = piece_y + row_index
                if board_x < 0 or board_x >= self.board_width or board_y >= self.board_height:
                    return True
                if board_y >= 0 and self.board[board_y][board_x]:
                    return True
        return False

    def _draw_cell(self, renderer, column_index: int, row_index: int) -> None:
        renderer.draw_box(
            column_index * self.cell_size,
            self.top_offset + row_index * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
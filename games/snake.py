"""Snake for the Pico arcade console."""

import random

from games.base import GameBase


class SnakeGame(GameBase):
    """Grid-based snake game using the shared engine contract."""

    name = "Snake"

    def __init__(self, config) -> None:
        self.config = config
        self.cell_size = 4
        self.top_offset = 10
        self.tick_rate = 6
        self.reset()

    def reset(self) -> None:
        self.columns = self.config.width // self.cell_size
        self.rows = (self.config.height - self.top_offset) // self.cell_size
        self.snake = [(self.columns // 2, self.rows // 2)]
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self._tick = 0
        self.food = self._spawn_food()

    def update(self, input_manager) -> None:
        if self.game_over:
            if input_manager.just_pressed("player1", "button"):
                self.reset()
            return

        self._update_direction(input_manager)
        self._tick += 1
        if self._tick % self.tick_rate != 0:
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        if self._is_wall_hit(new_head) or new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
            return

        self.snake.pop()

    def render(self, renderer) -> None:
        renderer.draw_text("SNAKE", 0, 0)
        renderer.draw_text(str(self.score), 56, 0)
        renderer.draw_box(0, self.top_offset, self.config.width, self.config.height - self.top_offset)

        food_x, food_y = self.food
        renderer.draw_box(
            food_x * self.cell_size,
            self.top_offset + food_y * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

        for segment_x, segment_y in self.snake:
            renderer.draw_box(
                segment_x * self.cell_size,
                self.top_offset + segment_y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )

        if self.game_over:
            renderer.draw_centered_text("Game Over", 22)
            renderer.draw_centered_text("Press A to restart", 34)

    def _update_direction(self, input_manager) -> None:
        x_value = input_manager.current["player1"]["x"]
        y_value = input_manager.current["player1"]["y"]

        if x_value < 22000 and self.direction != (1, 0):
            self.pending_direction = (-1, 0)
        elif x_value > 43000 and self.direction != (-1, 0):
            self.pending_direction = (1, 0)
        elif y_value < 22000 and self.direction != (0, 1):
            self.pending_direction = (0, -1)
        elif y_value > 43000 and self.direction != (0, -1):
            self.pending_direction = (0, 1)

    def _spawn_food(self):
        occupied = set(self.snake)
        while True:
            food = (random.randint(0, self.columns - 1), random.randint(0, self.rows - 1))
            if food not in occupied:
                return food

    def _is_wall_hit(self, position) -> bool:
        x, y = position
        return x < 0 or y < 0 or x >= self.columns or y >= self.rows

    def get_score(self) -> int:
        return self.score
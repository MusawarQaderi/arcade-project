"""Pong for the Pico arcade console."""

from games.base import GameBase


class PongGame(GameBase):
    """Simple two-player Pong implementation."""

    name = "Pong"

    def __init__(self, config) -> None:
        self.config = config
        self.paddle_width = 2
        self.paddle_height = 12
        self.ball_size = 2
        self.score_limit = 5
        self.reset()

    def reset(self) -> None:
        self.left_y = (self.config.height - self.paddle_height) // 2
        self.right_y = (self.config.height - self.paddle_height) // 2
        self.left_score = 0
        self.right_score = 0
        self.ball_x = (self.config.width - self.ball_size) // 2
        self.ball_y = (self.config.height - self.ball_size) // 2
        self.ball_dx = 1
        self.ball_dy = 1
        self.game_over = False

    def update(self, input_manager) -> None:
        if self.game_over:
            if input_manager.just_pressed("player1", "button"):
                self.reset()
            return

        self._move_paddles(input_manager)
        self._move_ball()

    def render(self, renderer) -> None:
        renderer.draw_text("PONG", 0, 0)
        renderer.draw_text(str(self.left_score), 40, 0)
        renderer.draw_text(str(self.right_score), 80, 0)
        renderer.draw_box(2, self.left_y, self.paddle_width, self.paddle_height)
        renderer.draw_box(self.config.width - 4, self.right_y, self.paddle_width, self.paddle_height)
        renderer.draw_box(self.ball_x, self.ball_y, self.ball_size, self.ball_size)
        renderer.draw_box(0, 10, self.config.width, self.config.height - 10)

        if self.game_over:
            renderer.draw_centered_text("Game Over", 24)
            renderer.draw_centered_text("Press A to restart", 36)

    def _move_paddles(self, input_manager) -> None:
        self.left_y = self._clamp_paddle(self.left_y, input_manager.current["player1"]["y"])
        self.right_y = self._clamp_paddle(self.right_y, input_manager.current["player2"]["y"])

    def _clamp_paddle(self, position, axis_value):
        center = self.config.height // 2
        if axis_value < 22000:
            position -= 2
        elif axis_value > 43000:
            position += 2

        if position < 10:
            return 10

        max_position = self.config.height - self.paddle_height - 1
        if position > max_position:
            return max_position

        if abs(axis_value - 32768) < 4000:
            return position

        if axis_value < 32768:
            return max(10, position - 1)

        return min(max_position, position + 1)

    def _move_ball(self) -> None:
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= 10 or self.ball_y >= self.config.height - self.ball_size:
            self.ball_dy = -self.ball_dy
            self.ball_y = max(10, min(self.ball_y, self.config.height - self.ball_size))

        if self.ball_x <= 4:
            if self.left_y <= self.ball_y <= self.left_y + self.paddle_height:
                self.ball_dx = 1
            else:
                self.right_score += 1
                self._serve(direction=1)

        if self.ball_x >= self.config.width - 6:
            if self.right_y <= self.ball_y <= self.right_y + self.paddle_height:
                self.ball_dx = -1
            else:
                self.left_score += 1
                self._serve(direction=-1)

        if self.left_score >= self.score_limit or self.right_score >= self.score_limit:
            self.game_over = True

    def _serve(self, direction):
        self.ball_x = (self.config.width - self.ball_size) // 2
        self.ball_y = (self.config.height - self.ball_size) // 2
        self.ball_dx = direction
        self.ball_dy = 1 if self.ball_dy >= 0 else -1

    def get_score(self) -> int:
        return max(self.left_score, self.right_score)
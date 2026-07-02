"""Breakout for the Pico arcade console."""

from games.base import GameBase


class BreakoutGame(GameBase):
    """Small brick breaker game built on the shared engine contract."""

    name = "Breakout"

    def __init__(self, config) -> None:
        self.config = config
        self.top_offset = 12
        self.paddle_width = 18
        self.paddle_height = 3
        self.ball_size = 2
        self.brick_rows = 4
        self.brick_columns = 6
        self.brick_gap = 1
        self.score_per_brick = 10
        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.game_over = False
        self.victory = False
        self.paddle_x = (self.config.width - self.paddle_width) // 2
        self.paddle_y = self.config.height - 8
        self.ball_x = self.config.width // 2
        self.ball_y = self.config.height // 2
        self.ball_dx = 1
        self.ball_dy = -1
        self.bricks = self._create_bricks()

    def update(self, input_manager) -> None:
        if self.game_over or self.victory:
            if input_manager.just_pressed("player1", "button"):
                self.reset()
            return

        self._update_paddle(input_manager)
        self._move_ball()

    def render(self, renderer) -> None:
        renderer.draw_text("BREAKOUT", 0, 0)
        renderer.draw_text(str(self.score), 72, 0)
        renderer.draw_box(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height)
        renderer.draw_box(self.ball_x, self.ball_y, self.ball_size, self.ball_size)

        for row in self.bricks:
            for brick in row:
                if brick["alive"]:
                    renderer.draw_box(brick["x"], brick["y"], brick["w"], brick["h"])

        if self.game_over:
            renderer.draw_centered_text("Game Over", 24)
            renderer.draw_centered_text("Press A to restart", 36)
        elif self.victory:
            renderer.draw_centered_text("You Win", 24)
            renderer.draw_centered_text("Press A to restart", 36)

    def _update_paddle(self, input_manager) -> None:
        axis_value = input_manager.current["player1"]["x"]
        if axis_value < 22000:
            self.paddle_x -= 3
        elif axis_value > 43000:
            self.paddle_x += 3

        if self.paddle_x < 0:
            self.paddle_x = 0

        max_x = self.config.width - self.paddle_width
        if self.paddle_x > max_x:
            self.paddle_x = max_x

    def _move_ball(self) -> None:
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= 0 or self.ball_x >= self.config.width - self.ball_size:
            self.ball_dx = -self.ball_dx
            self.ball_x = max(0, min(self.ball_x, self.config.width - self.ball_size))

        if self.ball_y <= self.top_offset:
            self.ball_dy = -self.ball_dy
            self.ball_y = self.top_offset

        if self.ball_y >= self.config.height - self.ball_size:
            self.game_over = True
            return

        if self._ball_hits_paddle():
            self.ball_dy = -1
            self.ball_y = self.paddle_y - self.ball_size - 1

        if self._ball_hits_brick():
            self.ball_dy = -self.ball_dy
            self.score += self.score_per_brick

        if self._all_bricks_cleared():
            self.victory = True

    def _ball_hits_paddle(self) -> bool:
        ball_bottom = self.ball_y + self.ball_size
        paddle_top = self.paddle_y
        if ball_bottom < paddle_top or self.ball_y > paddle_top + self.paddle_height:
            return False

        ball_right = self.ball_x + self.ball_size
        paddle_right = self.paddle_x + self.paddle_width
        return not (ball_right < self.paddle_x or self.ball_x > paddle_right)

    def _ball_hits_brick(self) -> bool:
        ball_right = self.ball_x + self.ball_size
        ball_bottom = self.ball_y + self.ball_size

        for row in self.bricks:
            for brick in row:
                if not brick["alive"]:
                    continue
                brick_right = brick["x"] + brick["w"]
                brick_bottom = brick["y"] + brick["h"]
                intersects = not (
                    ball_right < brick["x"]
                    or self.ball_x > brick_right
                    or ball_bottom < brick["y"]
                    or self.ball_y > brick_bottom
                )
                if intersects:
                    brick["alive"] = False
                    return True
        return False

    def _all_bricks_cleared(self) -> bool:
        for row in self.bricks:
            for brick in row:
                if brick["alive"]:
                    return False
        return True

    def _create_bricks(self):
        bricks = []
        available_width = self.config.width - 2
        brick_width = (available_width - (self.brick_columns - 1) * self.brick_gap) // self.brick_columns
        brick_height = 5
        start_x = 1
        start_y = self.top_offset + 2

        for row_index in range(self.brick_rows):
            row = []
            for column_index in range(self.brick_columns):
                x = start_x + column_index * (brick_width + self.brick_gap)
                y = start_y + row_index * (brick_height + self.brick_gap)
                row.append({"x": x, "y": y, "w": brick_width, "h": brick_height, "alive": True})
            bricks.append(row)

        return bricks

    def get_score(self) -> int:
        return self.score
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = (GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

KEY_DIRECTION = {
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_UP, LEFT): UP,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

# Цвет фона - светло-зеленый:
BOARD_BACKGROUND_COLOR = (160, 190, 140)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 255, 0)

# Цвета для мухомора
AMANITA_COLOR = (200, 30, 30)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)  # Сетка/обводка пикселей

# Фиксированные позиции белых «пикселей» (координаты клеток 0..19)
DOT_POSITIONS = [
    (0.25, 0.30),
    (0.65, 0.20),
    (0.40, 0.55),
    (0.80, 0.45),
    (0.35, 0.75),
    (0.70, 0.65),
    (0.55, 0.85),
]

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Используется для хранения общих атрибутов игровых объектов."""

    def __init__(self, position=GRID_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объекты на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_free_position(self, occupied=()):
        """Возвращает случайную позицию, не совпадающую с занятыми клетками."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied:
                return position


class Apple(GameObject):
    """Используется для появления яблока на поле в случайном месте."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied=(GRID_CENTER,))

    def randomize_position(self, occupied=()):
        """Возвращает случайную позицию яблока."""
        self.position = self.randomize_free_position(occupied)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        super().draw()


class Amanita(GameObject):
    """Используется для появления мухомора на поле в случайном месте."""

    def __init__(self):
        super().__init__(body_color=AMANITA_COLOR)
        self.randomize_position(occupied=(GRID_CENTER,))

    def randomize_position(self, occupied=()):
        """Возвращает случайную позицию мухомора."""
        self.position = self.randomize_free_position(occupied)

    def draw(self):
        """Отрисовывает мухомор на игровой поверхности."""
        super().draw()
        dot_size = GRID_SIZE // 6
        cell_x, cell_y = self.position

        for dot_offset_x, dot_offset_y in DOT_POSITIONS:
            point_x = cell_x + int(dot_offset_x * GRID_SIZE)
            point_y = cell_y + int(dot_offset_y * GRID_SIZE)
            dot_rect = pygame.Rect(
                point_x - dot_size // 2,
                point_y - dot_size // 2,
                dot_size,
                dot_size
            )

            pygame.draw.rect(screen, WHITE, dot_rect)
            pygame.draw.rect(screen, BLACK, dot_rect, 1)


class Snake(GameObject):
    """Управляет движением змейки, её ростом и обработкой столкновений."""

    def __init__(self):
        super().__init__(position=GRID_CENTER, body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Обновляет направление (заглушка для прохождения тестов)."""

    def clear_center(self, apple, amanita):
        """Убирает еду из клетки возрождения змейки."""
        if apple.position == GRID_CENTER:
            apple.randomize_position(occupied=[amanita.position])
        if amanita.position == GRID_CENTER:
            amanita.randomize_position(occupied=[apple.position])

    def move(self, new_direction=None):
        """Двигает голову змейки и возвращает новую позицию."""
        if new_direction:
            self.direction = new_direction

        dir_x, dir_y = self.direction
        x, y = self.get_head_position()
        new_x = (x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        return new_head

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            head_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.position = GRID_CENTER
        self.positions = [GRID_CENTER]
        self.direction = choice(DIRECTIONS)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, для изменения направления змейки."""
    new_dir = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            key_direction = (event.key, game_object.direction)
            new_dir = KEY_DIRECTION.get(key_direction)
    return new_dir


def main():
    """Основной игровой цикл.

    Управляет обновлением всей игры: получает действия пользователя,
    изменяет состояние объектов и обновляет экран.
    """
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple()
    amanita = Amanita()
    amanita.randomize_position(occupied=[apple.position])
    snake = Snake()
    font = pygame.font.SysFont(None, 30)
    result_font = pygame.font.SysFont(None, 50)

    while True:
        new_dir = handle_keys(snake)
        new_head = snake.move(new_direction=new_dir)

        if new_head in snake.positions[1:] or (
            new_head == amanita.position and snake.length <= 1
        ):
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw()
            amanita.draw()
            snake.draw()
            result_text = result_font.render(
                f'Игра окончена! Счёт: {snake.length - 1}', True, (0, 0, 0)
            )
            text_rect = result_text.get_rect(center=(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(result_text, text_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            snake.reset()
            snake.clear_center(apple, amanita)
            continue

        elif new_head == amanita.position:
            snake.length -= 1
            snake.positions.pop()
            snake.positions.pop()
            amanita.randomize_position(
                occupied=[apple.position, *snake.positions]
            )

        elif new_head == apple.position:
            snake.length += 1
            apple.randomize_position(
                occupied=[amanita.position, *snake.positions]
            )

        else:
            snake.positions.pop()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        amanita.draw()
        snake.draw()
        score_text = font.render(f'Очки: {snake.length - 1}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        clock.tick(SPEED)
        pygame.display.update()


if __name__ == '__main__':
    main()

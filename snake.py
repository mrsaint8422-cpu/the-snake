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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

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
    """Класс GameObject используется для хранения общих атрибутов
    игровых объектов.
    """

    def __init__(self, position=GRID_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс Apple используется для появления яблока
    на поле в случайном месте.
    """

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake управляет движением змейки,
    её ростом и обработкой столкновений.
    """

    def __init__(self):
        super().__init__(position=GRID_CENTER, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [GRID_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Обновляет позицию змейки, обрабатывает столкновение, добавляет
        новую голову в начало списка positions и удаляет последний элемент,
        если длина змейки не увеличилась.
        """
        x, y = self.get_head_position()
        new_x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if new_head in self.positions[1:]:
            self.reset()
            apple.randomize_position()
        elif new_head == apple.position:
            self.length += 1
            apple.randomize_position()
        else:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            head_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.position = GRID_CENTER
        self.positions = [GRID_CENTER]
        self.direction = choice(DIRECTIONS)
        self.last = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл, управляет обновлением всей игры:
    получает действия пользователя, изменяет состояние
    объектов и обновляет экран.
    """
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        clock.tick(SPEED)
        pygame.display.update()


if __name__ == '__main__':
    main()

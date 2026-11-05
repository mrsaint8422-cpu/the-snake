import pygame
import sys
import math

# --- Настройки игры ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_W = 20
GRID_H = 20

CELL_W = SCREEN_WIDTH // GRID_W  # 32 пикселя
CELL_H = SCREEN_HEIGHT // GRID_H  # 24 пикселя

# Цвета
RED = (200, 30, 30)
WHITE = (255, 255, 255)
DARK_RED = (140, 20, 20)
BLACK = (20, 20, 20)

# Позиция клетки, где будет мухомор (0..19)
cell_x = 10
cell_y = 15

# Фиксированные позиции точек (в относительных координатах 0.0–1.0)
# Подбирал так, чтобы они были в разброс и не слипались
DOT_POSITIONS = [
    (0.25, 0.30),
    (0.65, 0.20),
    (0.40, 0.55),
    (0.80, 0.45),
    (0.35, 0.75),
    (0.70, 0.65),
    (0.55, 0.85),
]

def draw_mushroom_in_cell(surface, cx, cy):
    """Рисует мухомор в одной конкретной клетке (cx, cy)."""
    left = cx * CELL_W
    top = cy * CELL_H

    # Размер точки: 1/6 от размера клетки — мелкие, как ты хотел
    dot_w = CELL_W // 6
    dot_h = CELL_H // 6

    # Красная шляпка — заполняем всю клетку
    pygame.draw.rect(surface, RED, (left, top, CELL_W, CELL_H))

    # Тёмная рамка вокруг клетки — отделяет мухомор от соседей
    pygame.draw.rect(surface, DARK_RED, (left, top, CELL_W, CELL_H), 2)

    # Белые точки (в разброс, не близко друг к другу)
    for dx, dy in DOT_POSITIONS:
        px = left + int(dx * CELL_W)
        py = top + int(dy * CELL_H)

        # Центрируем точку по рассчитанной позиции
        rect = pygame.Rect(
            px - dot_w // 2,
            py - dot_h // 2,
            dot_w,
            dot_h
        )

        # Не даём точке вылезти за границы клетки
        rect.clamp_ip(pygame.Rect(left, top, CELL_W, CELL_H))

        pygame.draw.rect(surface, WHITE, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # чёрная обводка для пиксельности

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Мухомор: мелкие точки в разброс")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Фон — светло‑зелёный (как трава)
        screen.fill((160, 190, 140))

        # Сетка (можно убрать, если у тебя она уже есть в игре)
        for x in range(GRID_W + 1):
            gx = x * CELL_W
            pygame.draw.line(screen, (120, 140, 110), (gx, 0), (gx, SCREEN_HEIGHT), 1)
        for y in range(GRID_H + 1):
            gy = y * CELL_H
            pygame.draw.line(screen, (120, 140, 110), (0, gy), (SCREEN_WIDTH, gy), 1)

        # Рисуем мухомор только в одной клетке
        draw_mushroom_in_cell(screen, cell_x, cell_y)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
import pygame
import random

# 初始化pygame
pygame.init()

# 設置遊戲視窗大小
WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("俄羅斯方塊")

# 顏色設置
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE]

# 方塊形狀 (7種)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# 格子大小
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# 設置時鐘
clock = pygame.time.Clock()

# 創建遊戲函數
def create_shape():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return shape, color

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_shape(shape, color, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (x + j * GRID_SIZE, y + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision(grid, shape, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or grid[y + i][x + j]:
                    return True
    return False

def clear_lines(grid):
    for i in range(GRID_HEIGHT - 1, -1, -1):
        if all(grid[i]):
            grid.pop(i)
            grid.insert(0, [0] * GRID_WIDTH)

def main():
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    shape, color = create_shape()
    x, y = GRID_WIDTH // 2 - len(shape[0]) // 2, 0
    game_over = False

    while not game_over:
        screen.fill((0, 0, 0))
        draw_grid()
        draw_shape(shape, color, x * GRID_SIZE, y * GRID_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, shape, x - 1, y):
                        x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(grid, shape, x + 1, y):
                        x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(grid, shape, x, y + 1):
                        y += 1
                elif event.key == pygame.K_UP:
                    new_shape = [list(row) for row in zip(*shape[::-1])]
                    if not check_collision(grid, new_shape, x, y):
                        shape = new_shape

        if not check_collision(grid, shape, x, y + 1):
            y += 1
        else:
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell:
                        grid[y + i][x + j] = 1
            clear_lines(grid)
            shape, color = create_shape()
            x, y = GRID_WIDTH // 2 - len(shape[0]) // 2, 0
            if check_collision(grid, shape, x, y):
                game_over = True

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()


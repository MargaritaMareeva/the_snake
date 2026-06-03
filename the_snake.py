from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw_rect(self, position) -> None:
        """Отрисовывает квадрат в указанной позиции."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Абстрактный метод для отрисовки объекта."""
        ...


class Apple(GameObject):
    """Яблоко, которое ест змейка."""

    def __init__(self, occupied=None) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=None) -> None:
        """Устанавливает случайную позицию яблока на игровом поле."""
        if occupied is None:
            occupied = []
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied:
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Змейка, управляемая игроком."""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self, next_direction=None) -> None:
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def move(self) -> None:
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            self.draw_rect(position)

        # Отрисовка головы змейки
        self.draw_rect(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None


def handle_keys(game_object: Snake) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            # Выход из игры по клавише ESC
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            # Обработка направления движения
            key_mapping = {
                pg.K_UP: (UP, DOWN),
                pg.K_DOWN: (DOWN, UP),
                pg.K_LEFT: (LEFT, RIGHT),
                pg.K_RIGHT: (RIGHT, LEFT)
            }
            if event.key in key_mapping:
                new_direction, forbidden = key_mapping[event.key]
                if game_object.direction != forbidden:
                    game_object.update_direction(new_direction)


def main() -> None:
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pg.init()

    # Создание экземпляров классов:
    snake = Snake()
    apple = Apple(occupied=snake.positions)

    # Очищаем экран: заливаем цветом фона
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        # Обработка нажатий клавиш:
        handle_keys(snake)

        # Обновление направления движения змейки:
        snake.update_direction()

        # Движение змейки:
        snake.move()

        # Проверка: столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка: совпадают ли координаты головы с любой частью тела
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов и обновление экрана
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

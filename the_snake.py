from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption(f'Snake speed: {str(SPEED)}. Pause: press ESC')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(
            self,
            body_color=BOARD_BACKGROUND_COLOR,
            position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода для отрисовки объекта на игровом поле."""
        pass

    def pydraw(self, color, rect_value, value):
        """Метод для отрисовки элементов."""
        pygame.draw.rect(screen, color, rect_value, value)


class Apple(GameObject):
    """Класс, который описывает яблоко."""

    def __init__(
            self,
            body_color=APPLE_COLOR,
            position=None):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод, определяющий случайное положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод, отрисовывающий яблоко"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )

        self.pydraw(self.body_color, rect, 0)
        self.pydraw(BORDER_COLOR, rect, 1)
        # pygame.draw.rect(screen, self.body_color, rect)
        # pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, который описывает яблоко."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

    def get_head_position(self):
        """Метод, возвращающий позицию головы."""
        return self.positions[0]

    def update_direction(self):
        """Метод, обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, necessary_class):
        """Метод, обновляющий позицию змейки."""
        self.head_snake = self.get_head_position()
        new_coordinate_dx = ((self.head_snake[0]
                             + self.direction[0]
                             * GRID_SIZE)
                             % SCREEN_WIDTH)
        new_coordinate_dy = ((self.head_snake[1]
                             + self.direction[1]
                             * GRID_SIZE)
                             % SCREEN_HEIGHT)

        # new_coordinate_dx = (self.head_snake[0]
        #                      + self.direction[0]
        #                      * GRID_SIZE)
        # new_coordinate_dy = (self.head_snake[1]
        #                      + self.direction[1]
        #                      * GRID_SIZE)

        self.new_head_snake = (new_coordinate_dx, new_coordinate_dy)

        # if self.new_head_snake[0] < 0 and self.direction == LEFT:
        #     self.new_head_snake = (SCREEN_WIDTH, self.new_head_snake[1])
        # elif (self.new_head_snake[0] == SCREEN_WIDTH
        #         and self.direction == RIGHT):
        #     self.new_head_snake = (0, self.new_head_snake[1])
        # elif self.head_snake[1] < 0 and self.direction == UP:
        #     self.new_head_snake = (self.new_head_snake[0], SCREEN_HEIGHT)
        # elif (self.new_head_snake[1] == SCREEN_HEIGHT
        #         and self.direction == DOWN):
        #     self.new_head_snake = (self.new_head_snake[0], 0)

        if self.new_head_snake == necessary_class.position:
            self.length += 1
            necessary_class.randomize_position()

        if self.new_head_snake in self.positions[2::]:
            self.reset()
        else:
            self.positions.insert(0, self.new_head_snake)
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()

    def reset(self):
        """Метод, возвращающий змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        choice_direction = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(choice_direction)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод, отрисовывающий змейку"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            self.pydraw(self.body_color, rect, 0)
            self.pydraw(BORDER_COLOR, rect, 1)
            # pygame.draw.rect(screen, self.body_color, rect)
            # pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        self.pydraw(self.body_color, head_rect, 0)
        self.pydraw(BORDER_COLOR, head_rect, 1)
        # pygame.draw.rect(screen, self.body_color, head_rect)
        # pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция, обрабатывающая нажатия клавиш,
    для изменения направления движения змейки.
    """
    dict_control = {(pygame.K_UP, LEFT): UP,
                    (pygame.K_UP, RIGHT): UP,
                    (pygame.K_DOWN, LEFT): DOWN,
                    (pygame.K_DOWN, RIGHT): DOWN,
                    (pygame.K_LEFT, UP): LEFT,
                    (pygame.K_LEFT, DOWN): LEFT,
                    (pygame.K_RIGHT, UP): RIGHT,
                    (pygame.K_RIGHT, DOWN): RIGHT
                    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key, game_object.direction) in dict_control:
                game_object.next_direction = dict_control[(
                    event.key, game_object.direction)]
            elif event.key == pygame.K_ESCAPE:
                pause()


def print_text(message, coordinate_x, coordinate_y, font_color, font_size=30):
    """Функция вывода текста на экран во время паузы."""
    font_type = pygame.font.SysFont('arial', font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (coordinate_x, coordinate_y))


def pause():
    """Фукнция паузы."""
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        print_text('Paused. Press Enter to continue',
                   150, (SCREEN_HEIGHT // 2),
                   (255, 255, 255), font_size=30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
            pygame.draw.rect(screen,
                             BOARD_BACKGROUND_COLOR,
                             pygame.Rect(140, 240, 380, 40))
        pygame.display.update()


def main():
    """Функция, описывающая логику игры."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

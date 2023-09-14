import pygame, sys, random
import numpy as np

class UI():
    def __init__(self, w, h):
        self.width = w
        self.heigth = h
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((self.width, self.heigth))
        self.background = pygame.Surface((self.width, self.heigth))
        self.background.fill(pygame.Color('#000000'))
        self.top = pygame.Surface((self.width, self.heigth))
        self.top.fill(pygame.Color('#2b2b2b'))

    def draw(self, points, snake_parts):
        self.screen.blit(self.top, (0, 0))
        self.screen.blit(self.background, (0, 50))
        self.draw_points(pygame.font.Font('font/Pixeltype.ttf', 50), (200, 200, 0), points)
        self.draw_snake(snake_parts)

    def draw_points(self, font, text_color, points):
        surface = font.render(f'Score: {points}', True, text_color)
        score_rect = surface.get_rect(center=(self.width / 2, 30))
        self.screen.blit(surface, score_rect)

    def draw_snake(self, snake_parts):
        big_size = 50
        small_size = 44
        big_rect = pygame.Surface((big_size, big_size))
        big_rect.fill(pygame.Color('#52100b'))
        small_rect = pygame.Surface((small_size, small_size))
        small_rect.fill(pygame.Color('#eb4336'))

        for p in snake_parts:
            self.screen.blit(big_rect, (p[0] * big_size, p[1] * big_size + 50))
            self.screen.blit(small_rect, (p[0] * big_size + int((big_size - small_size) / 2), p[1] * big_size + int((big_size - small_size) / 2) + 50))



class Snake():
    def __init__(self, x, y, game_width, game_height):
        self.x = x
        self.y = y
        self.game_width = game_width
        self.game_height = game_height
        self.length = 3
        self.parts = []
        self.dir = 'left'
        self.last_dir = 'left'
        for i in range(self.length):
            self.parts.append([self.x + i, self.y])

    def change_dir(self, dir):
        self.dir = dir
        if self.dir == 'left':
            self.dir = 'right' if self.last_dir == 'right' else 'left'
        elif self.dir == 'right':
            self.dir = 'left' if self.last_dir == 'left' else 'right'
        elif self.dir == 'up':
            self.dir = 'down' if self.last_dir == 'down' else 'up'
        elif self.dir == 'down':
            self.dir = 'up' if self.last_dir == 'up' else 'down'

        self.last_dir = self.dir

    def move(self):
        head_x = self.parts[0][0]
        head_y = self.parts[0][1]
        if self.dir == 'right':
            self.parts.insert(0, [head_x + 1, head_y])
        elif self.dir == 'left':
            self.parts.insert(0, [head_x - 1, head_y])
        elif self.dir == 'up':
            self.parts.insert(0, [head_x, head_y - 1])
        elif self.dir == 'down':
            self.parts.insert(0, [head_x, head_y + 1])

        self.parts.pop()


    def grow(self):
        tail = self.parts[self.length - 1]
        self.parts.append(tail)
        self.length += 1

    def is_collision(self):
        head = self.parts[0]
        for i in range(1, self.parts):
            if self.parts[i] == head:
                return True

        if head[0] + 1 >= self.game_width or head[0] <= 0:
            return True
        if head[1] + 1 >= self.game_height or head[1] <= 0:
            return True

        return False


class Apple():
    def __init__(self, snake_parts, game_width, game_height):
        self.snake_parts = snake_parts
        self.game_width = game_width
        self.game_height = game_height
        self.x, self.y = self.spawn()

    def spawn(self):
        is_spawn = False
        while not is_spawn:
            is_spawn = True
            x = random.randint(0, self.game_width)
            y = random.randint(0, self.game_height)

            for p in self.snake_parts:
                if x == p[0] and y == p[1]:
                    is_spawn = False
                    break

        return x, y


class Game_Logic():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_width = 600
        self.game_height = 550
        self.snake = Snake(5, 0, self.game_width / 50, self.game_height / 50)
        self.ui = UI(self.game_width, self.game_height)
        self.is_running = True
        self.points = 0
        self.current_game_speed, self.game_speed = 1, 1

    def game_loop(self):
        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.snake.change_dir('down')
                    elif event.key == pygame.K_d:
                        self.snake.change_dir('right')
                    elif event.key == pygame.K_a:
                        self.snake.change_dir('left')
                    elif event.key == pygame.K_w:
                        self.snake.change_dir('up')

            if self.current_game_speed <= 0:
                self.current_game_speed = self.game_speed
                self.snake.move()
            self.current_game_speed -= 0.1

            self.ui.draw(self.points, self.snake.parts)

            pygame.display.update()
            self.clock.tick(60)

game_logic = Game_Logic()
game_logic.game_loop()

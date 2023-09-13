import pygame, sys

class UI():
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.heigth = h
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((self.width, self.heigth))
        self.is_running = True
        self.background = pygame.Surface((self.width, self.heigth))
        self.background.fill(pygame.Color('#000000'))
        self.top = pygame.Surface((self.width, self.heigth))
        self.top.fill(pygame.Color('#2b2b2b'))
        self.points = 0

    def draw(self):
        self.screen.blit(self.top, (0, 0))
        self.screen.blit(self.background, (0, 50))
        self.draw_points(pygame.font.Font('font/Pixeltype.ttf', 50), (200, 200, 0))

    def draw_points(self, font, text_color):
        surface = font.render(f'Score: {self.points}', True, text_color)
        score_rect = surface.get_rect(center=(self.width / 2, 30))
        self.screen.blit(surface, score_rect)

    def game_loop(self):
        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    sys.exit()

            self.draw()

            pygame.display.update()
            self.clock.tick(60)


ui = UI(600, 600)
ui.game_loop()

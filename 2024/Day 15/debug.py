import numpy as np
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_CAPSLOCK

"""

Courtesy of ChatGPT

"""

# Constants
UP = np.array([-1, 0], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
RIGHT = np.array([0, 1], dtype=int)

TILE_SIZE = 15
FPS = 30
COLORS = {
    0: (255, 255, 255),  # Empty: White
    1: (0, 0, 0),        # Wall: Black
    2: (255, 165, 0),    # Box: Orange
    3: (0, 0, 255),      # Robot: Blue
    4: (169, 169, 169),  # Box (right part): Gray
}

pygame.init()

class WarehouseAnimation:
    def __init__(self, warehouse, movements):
        self.warehouse = warehouse
        self.movements = movements
        self.current_move_idx = 0
        self.running = True

        self.rows, self.cols = self.warehouse.map.shape
        self.window_width = self.cols * TILE_SIZE
        self.window_height = self.rows * TILE_SIZE
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def draw_warehouse(self):
        # Draw the warehouse map
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color = COLORS.get(self.warehouse.map[y, x], (255, 255, 255))
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Grid lines

                # If the robot is here, add the direction text
                if self.warehouse.map[y, x] == 3:
                    if self.current_move_idx < len(self.movements):
                        direction = self.movements[self.current_move_idx]
                        direction_char = {
                            tuple(UP): "^",
                            tuple(DOWN): "v",
                            tuple(LEFT): "<",
                            tuple(RIGHT): ">",
                        }[tuple(direction)]
                    else:
                        direction_char = " "  # No more moves

                    # Render the text inside the robot's square
                    text = self.font.render(direction_char, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                    self.screen.blit(text, text_rect)

    def next_step(self):
        if self.current_move_idx < len(self.movements):
            self.warehouse.move(self.movements[self.current_move_idx])
            self.current_move_idx += 1

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))  # Clear screen
            self.draw_warehouse()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN and event.key == K_CAPSLOCK:

                    self.next_step()

            if pygame.key.get_pressed()[K_SPACE]:
                self.next_step()
                    

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
    
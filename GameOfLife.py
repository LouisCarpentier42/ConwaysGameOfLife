
import pygame
import numpy as np


class GameOfLife:

    def __init__(self, width, height, history_length):
        self.__grid = np.zeros((width, height))
        self.__history = []
        self.__history_length = history_length

        self.__area_to_check = 1 # Radius around a cell to consider as neighbor
        self.__nb_neighbors_stay_alive = [2, 3]
        self.__nb_neighbors_become_alive = [3]

        self.__color_alive = pygame.color.Color(0, 0, 0)
        self.__color_dead = pygame.color.Color(255, 255, 255)
        self.__color_grid = pygame.color.Color(100, 100, 100)
        self.__grid_border_width = 2

        self.__draw_nb_neighbours = False
        self.__nb_neighbors_color = pygame.color.Color(0, 150, 0)

        self.__draw_trail = False
        self.__trail_color_r = lambda _: 255
        self.__trail_color_g = lambda age_percent: 255*age_percent
        self.__trail_color_b = lambda age_percent: 255*age_percent

    def clear(self):
        self.__grid = np.zeros(self.__grid.shape)
        self.__history = []

    def randomize(self):
        self.clear()
        self.__grid = np.random.choice([0,1], size=self.__grid.shape)
        self.__history = []

    def is_alive(self, x, y):
        return self.__grid[x, y]

    def make_alive(self, x, y):
        self.__grid[x, y] = True

    def is_dead(self, x, y):
        return not self.__grid[x, y]

    def make_dead(self, x, y):
        self.__grid[x, y] = False

    def get_nb_neighbors_alive(self, x, y):
        nb_neighbors_alive = 0
        for i in range(x - self.__area_to_check, x + self.__area_to_check + 1):
            for j in range(y - self.__area_to_check, y + self.__area_to_check + 1):
                nb_neighbors_alive += self.is_alive(i % self.__grid.shape[0], j % self.__grid.shape[1])
        return int(nb_neighbors_alive - self.is_alive(x, y))

    def next(self):
        next_grid = np.copy(self.__grid)
        for x in range(self.__grid.shape[0]):
            for y in range(self.__grid.shape[1]):
                nb_neighbors_alive = self.get_nb_neighbors_alive(x, y)

                if self.is_alive(x, y) and nb_neighbors_alive not in self.__nb_neighbors_stay_alive:
                    next_grid[x, y] = False
                elif self.is_dead(x, y) and nb_neighbors_alive in self.__nb_neighbors_become_alive:
                    next_grid[x, y] = True

        self.__history.append(self.__grid)
        if len(self.__history) >= self.__history_length:
            self.__history = self.__history[1:]
        self.__grid = next_grid

    def randomize(self):
        self.__grid = np.random.choice([0, 1], size=self.__grid.shape)

    def add_glider(self, x, y):
        for x_shift, y_shift in [[-1,0], [0, 1], [1,1], [1,0], [1,-1]]:
            self.make_alive(x + x_shift, y + y_shift)

    def add_penta_decathlon(self, x, y):
        for x_shift, y_shift in [[-4, 0], [-3,-2], [-2,-3], [-1,-4], [0,-4], [1,-4], [2,-3], [3,-2], [4,0],
                                 [-4, 1], [-3,3], [-2,4], [-1,5], [0,5], [1,5], [2,4], [3,3], [4,1]]:
            self.make_alive(x + x_shift, y + y_shift)

    def draw(self, screen):
        block_width = screen.get_width() / self.__grid.shape[0]
        block_height = screen.get_width() / self.__grid.shape[1]

        for x in range(self.__grid.shape[0]):
            for y in range(self.__grid.shape[1]):
                rect = pygame.Rect(x * block_width, y * block_height, block_width, block_height)
                if self.is_alive(x, y):
                    pygame.draw.rect(screen, self.__color_alive, rect)
                else:
                    pygame.draw.rect(screen, self.__color_dead, rect)

        if self.__draw_trail:
            for x in range(self.__grid.shape[0]):
                for y in range(self.__grid.shape[1]):
                    if self.is_alive(x, y):
                        continue
                    for i in range(len(self.__history)-1,-1, -1):
                        if self.__history[i][x, y]:
                            rect = pygame.Rect(x * block_width, y * block_height, block_width, block_height)
                            age_percent = 1 - (i / len(self.__history))
                            color = pygame.color.Color(
                                int(self.__trail_color_r(age_percent)),
                                int(self.__trail_color_g(age_percent)),
                                int(self.__trail_color_b(age_percent)))
                            pygame.draw.rect(screen, color, rect)
                            break

        if self.__draw_nb_neighbours:
            font = pygame.font.Font('fonts/verdana.ttf', 16)
            for x in range(self.__grid.shape[0]):
                for y in range(self.__grid.shape[1]):
                    nb_neighbors_alive = self.get_nb_neighbors_alive(x, y)
                    text = font.render(str(nb_neighbors_alive), True, pygame.color.Color(self.__nb_neighbors_color))
                    textRect = text.get_rect()
                    textRect.center = (x * block_width + (block_width // 2), y * block_height + (block_height // 2))
                    screen.blit(text, textRect)

        for i in range(self.__grid.shape[0]):
            pygame.draw.rect(screen, self.__color_grid, pygame.Rect(i * block_width, 0, self.__grid_border_width, screen.get_height()))
        pygame.draw.rect(screen, self.__color_grid, pygame.Rect(screen.get_width()-self.__grid_border_width, 0, self.__grid_border_width, screen.get_height()))

        for i in range(self.__grid.shape[1]):
            pygame.draw.rect(screen, self.__color_grid, pygame.Rect(0, i * block_height, screen.get_width(), self.__grid_border_width))
        pygame.draw.rect(screen, self.__color_grid, pygame.Rect(0, screen.get_height()-self.__grid_border_width, screen.get_width(), self.__grid_border_width))

    def toggle_draw_nb_neighbors(self):
        self.__draw_nb_neighbours = not self.__draw_nb_neighbours

    def must_draw_nb_neighbours(self):
        return self.__draw_nb_neighbours

    def toggle_draw_trail(self):
        self.__draw_trail = not self.__draw_trail

    def must_draw_trail(self):
        return self.__draw_trail


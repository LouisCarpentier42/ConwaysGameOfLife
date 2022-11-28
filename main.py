

import sys, pygame
import numpy as np

from GameOfLife import GameOfLife
from Settings import Settings


BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
NB_CELLS_WIDTH = 10
NB_CELLS_HEIGHT = 10
BLOCK_SIZE = 40



def quit_game():
    pygame.quit()
    sys.exit()

KEYDOWN_EVENT_HANDLERS = {
    pygame.K_q : lambda _, __: quit_game(),
    pygame.K_ESCAPE : lambda _, __: quit_game(),
    pygame.K_k : lambda s, _: s.change_frame_rate(1),
    pygame.K_l : lambda s, _: s.change_frame_rate(-1),
    pygame.K_m : lambda s, _: s.change_automatic_mode(),
    pygame.K_SPACE : lambda _, g: g.next(),
    pygame.K_n : lambda _, g: g.change_draw_nb_neighbors(),
}

def main():

    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()

    settings = Settings(
        background_color=pygame.color.Color(100, 100, 100)
    )

    screen.fill(settings.background_color)
    pygame.display.update()

    game_of_life_screen_size_ratio = 0.95
    game_of_life_screen_width = min(screen.get_width(), screen.get_height()) * game_of_life_screen_size_ratio
    game_of_life_screen_rect = pygame.Rect(
        (screen.get_width() - game_of_life_screen_width) * 0.5,
        (screen.get_height() - game_of_life_screen_width) * 0.5,
        game_of_life_screen_width,
        game_of_life_screen_width
    )
    game_of_life_screen = screen.subsurface(game_of_life_screen_rect)
    game_of_life = GameOfLife(25, 25)
    # game_of_life.add_glider(2, 13)
    game_of_life.add_glider(15, 20)
    game_of_life.add_penta_decathlon(12, 12)

    while True:

        if settings.automatic_mode:
            game_of_life.next()
        game_of_life.draw(game_of_life_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in KEYDOWN_EVENT_HANDLERS.keys():
                    KEYDOWN_EVENT_HANDLERS[event.key](settings, game_of_life)

        pygame.display.update(game_of_life_screen_rect)
        if settings.automatic_mode:
            clock.tick(settings.frame_rate)





if __name__ == '__main__':
    main()
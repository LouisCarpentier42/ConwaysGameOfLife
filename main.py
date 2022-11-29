

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
    pygame.K_m : lambda s, g: (s.change_automatic_mode(), g.next()),
    pygame.K_SPACE : lambda _, g: g.next(),
    pygame.K_n : lambda _, g: g.change_draw_nb_neighbors(),
    pygame.K_t : lambda _, g: g.change_draw_trail(),
}

def main():

    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()

    settings = Settings(
        background_color=pygame.color.Color(100, 100, 100)
    )

    background = pygame.image.load('images/background.jpg')
    background_rect = pygame.transform.scale(background, (screen.get_width(), screen.get_height())).get_rect()
    screen.blit(pygame.transform.scale(background, (screen.get_width(), screen.get_height())), (0, 0))

    game_of_life_screen_size_ratio = 0.95
    game_of_life_screen_width = min(screen.get_width(), screen.get_height()) * game_of_life_screen_size_ratio
    game_of_life_screen_margin = (min(screen.get_width(), screen.get_height()) - game_of_life_screen_width)/2
    game_of_life_screen_rect = pygame.Rect(
        game_of_life_screen_margin,
        game_of_life_screen_margin,
        game_of_life_screen_width,
        game_of_life_screen_width
    )

    game_of_life_screen = screen.subsurface(game_of_life_screen_rect)
    game_of_life = GameOfLife(40, 40)
    # game_of_life.add_glider(2, 13)
    game_of_life.add_glider(15, 20)
    game_of_life.add_penta_decathlon(12, 12)

    settings_x = game_of_life_screen_width + game_of_life_screen_margin * 2
    settings_y = game_of_life_screen_margin
    key_icon_size = (60, 65)
    key_icon_vertical_spacing = 80
    key_icon_text_margin = 20

    text_color = pygame.color.Color(220, 220, 220)
    text = pygame.font.Font('fonts/verdana-bold.ttf', 45).render("Conway's Game of Life", True, text_color)
    textRect = text.get_rect()
    textRect.topleft = (settings_x, settings_y)
    screen.blit(text, textRect)
    settings_y += textRect.height + 10

    sub_text_lines = [
        'A simulation of a cellular automaton, in which each cell',
        'is either alive or dead. Evolution is guided by two rules',
        'SPACING',
        ' > If a cell is alive, then it stays alive if it has either',
        '    2 or 3 alive neighbours',
        'SPACING',
        ' > If a cell is dead, then it becomes alive if exactly',
        '    3 neighbours are alive',
    ]
    for line in sub_text_lines:
        if line == 'SPACING':
            settings_y += 10
            continue
        text = pygame.font.Font('fonts/verdana-bold.ttf', 20).render(line, True, text_color)
        textRect = text.get_rect()
        textRect.topleft = (settings_x, settings_y)
        screen.blit(text, textRect)
        settings_y += textRect.height

    settings_y += 35

    normal_font = pygame.font.Font('fonts/verdana-bold.ttf', 32)

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_q.png'), key_icon_size), [settings_x, settings_y])
    slash_text = pygame.font.Font('fonts/verdana-bold.ttf', 40).render('/', True, text_color)
    textRect = slash_text.get_rect()
    textRect.midleft = (settings_x + key_icon_size[0] + key_icon_text_margin * 0.7, settings_y + key_icon_size[1] // 2)
    screen.blit(slash_text, textRect)
    screen.blit(pygame.transform.scale(pygame.image.load('images/key_esc.png'), key_icon_size),
                [textRect.topright[0] + key_icon_text_margin * 0.7, settings_y])
    explanation_text = normal_font.render('Quit', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    textRect.midright[0] + key_icon_text_margin * 1.8 + key_icon_size[0], textRect.midright[1])
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_k.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Increase frame rate', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_l.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Decrease frame rate', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_t.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('(TODO) Toggle trail alive cells', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_n.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Toggle neighbour counts', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_m.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Toggle automatic mode', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    settings_y += key_icon_vertical_spacing

    space_bar_icon = pygame.transform.scale(pygame.image.load('images/key_space.png'), (key_icon_size[0] * 1.8, key_icon_size[1]))
    space_explanation_text = normal_font.render('Next step', True, text_color)
    space_explanation_text_rect = space_explanation_text.get_rect()
    space_explanation_text_rect.midleft = (settings_x + key_icon_size[0] * 1.8 + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(space_bar_icon, [settings_x, settings_y])
    screen.blit(space_explanation_text, space_explanation_text_rect)

    pygame.display.update()

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

        pygame.display.update()
        if settings.automatic_mode:
            clock.tick(settings.frame_rate)


if __name__ == '__main__':
    main()
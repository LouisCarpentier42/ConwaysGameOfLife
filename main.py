
import sys, pygame
import argparse

from GameOfLife import GameOfLife
from Settings import Settings


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
    pygame.K_n : lambda _, g: g.toggle_draw_nb_neighbors(),
    pygame.K_t : lambda _, g: g.toggle_draw_trail(),
    pygame.K_c : lambda _, g: g.clear(),
    pygame.K_r : lambda _, g: g.randomize(),
}

def get_grid_cell_clicked(clicked_pos, screen, grid_width, grid_height):
    x = clicked_pos[0] / (screen.get_width() / grid_width)
    y = clicked_pos[1] / (screen.get_height() / grid_height)
    if x < 0 or y < 0:
        return -1, -1
    return int(x), int(y)

def main(grid_width, grid_height, history_length):

    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()

    settings = Settings(
        background_color=pygame.color.Color(100, 100, 100)
    )

    background = pygame.image.load('images/background.jpg')
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
    game_of_life = GameOfLife(grid_width, grid_height, history_length)
    # game_of_life.add_glider(2, 13)
    # game_of_life.add_glider(15, 20)
    # game_of_life.add_penta_decathlon(12, 12)

    settings_x = game_of_life_screen_width + game_of_life_screen_margin * 2
    settings_y = game_of_life_screen_margin
    settings_on_off_x = screen.get_width() - game_of_life_screen_margin * 3
    key_icon_size = (60, 65)
    on_off_radius = 24
    on_off_border_thickness = 5
    color_on = pygame.color.Color(129, 214, 54)
    color_off = pygame.color.Color(214, 30, 30)
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
    explanation_text = normal_font.render('Toggle trail alive cells', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    on_off_toggle_trail_pos = [settings_on_off_x, settings_y + key_icon_size[1] // 2]
    pygame.draw.circle(screen, pygame.color.Color(0,0,0), on_off_toggle_trail_pos, on_off_radius+on_off_border_thickness, on_off_border_thickness)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_n.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Toggle neighbour counts', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    on_off_toggle_neighbor_pos = [settings_on_off_x, settings_y + key_icon_size[1] // 2]
    pygame.draw.circle(screen, pygame.color.Color(0,0,0), on_off_toggle_neighbor_pos, on_off_radius+on_off_border_thickness, on_off_border_thickness)
    settings_y += key_icon_vertical_spacing

    screen.blit(pygame.transform.scale(pygame.image.load('images/key_m.png'), key_icon_size), [settings_x, settings_y])
    explanation_text = normal_font.render('Toggle automatic mode', True, text_color)
    explanation_text_rect = explanation_text.get_rect()
    explanation_text_rect.midleft = (
    settings_x + key_icon_size[0] + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(explanation_text, explanation_text_rect)
    on_off_toggle_mode_pos = [settings_on_off_x, settings_y + key_icon_size[1] // 2]
    pygame.draw.circle(screen, pygame.color.Color(0,0,0), on_off_toggle_mode_pos, on_off_radius+on_off_border_thickness, on_off_border_thickness)
    settings_y += key_icon_vertical_spacing

    space_bar_icon = pygame.transform.scale(pygame.image.load('images/key_space.png'), (key_icon_size[0] * 1.8, key_icon_size[1]))
    space_explanation_text = normal_font.render('Next step', True, text_color)
    space_explanation_text_rect = space_explanation_text.get_rect()
    space_explanation_text_rect.midleft = (settings_x + key_icon_size[0] * 1.8 + key_icon_text_margin, settings_y + key_icon_size[1] // 2)
    screen.blit(space_bar_icon, [settings_x, settings_y])
    screen.blit(space_explanation_text, space_explanation_text_rect)

    pygame.display.update()

    add_glider = False
    add_penta_decathlon = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in KEYDOWN_EVENT_HANDLERS.keys():
                    KEYDOWN_EVENT_HANDLERS[event.key](settings, game_of_life)
                elif event.key == pygame.K_g:
                    add_glider = True
                elif event.key == pygame.K_p:
                    add_penta_decathlon = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shifted_pos = (event.pos[0] - game_of_life_screen_margin, event.pos[1] - game_of_life_screen_margin)
                (x, y) = get_grid_cell_clicked(shifted_pos, game_of_life_screen, grid_width, grid_height)
                if 0 <= x < grid_width and 0 <= y < grid_height:
                    if event.button == 1:
                        if add_glider:
                            game_of_life.add_glider(x, y)
                        elif add_penta_decathlon:
                            game_of_life.add_penta_decathlon(x, y)
                        else:
                            game_of_life.make_alive(x, y)
                    else:
                        game_of_life.make_dead(x, y)
                add_glider = False
                add_penta_decathlon = False


        if settings.automatic_mode:
            game_of_life.next()
        game_of_life.draw(game_of_life_screen)

        pygame.draw.circle(screen,
                           color_on if game_of_life.must_draw_trail() else color_off,
                           on_off_toggle_trail_pos,
                           on_off_radius)
        pygame.draw.circle(screen,
                           color_on if game_of_life.must_draw_nb_neighbours() else color_off,
                           on_off_toggle_neighbor_pos,
                           on_off_radius)
        pygame.draw.circle(screen,
                           color_on if settings.automatic_mode else color_off,
                           on_off_toggle_mode_pos,
                           on_off_radius)

        pygame.display.update()

        if settings.automatic_mode:
            clock.tick(settings.frame_rate)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument('-width', dest='width',
                        type=int, default=25,
                        help='Number of cells in the horizontal direction.')
    parser.add_argument('-height', dest='height',
                        type=int, default=25,
                        help='Number of cells in the vertical direction.')
    parser.add_argument('-history', dest='history',
                        type=int, default=10,
                        help='Number of past configurations to remember.')

    args = parser.parse_args()
    main(args.width, args.height, args.history)
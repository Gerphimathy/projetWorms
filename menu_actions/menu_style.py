import pygame


def default_menu_style():
    # pygame display style

    # IMPORTANT: Font must be BELOW background, otherwise the background will cover the font
    return {
        'background_color': (120, 120, 120),
        'background_image': None,
        'font': pygame.font.Font('assets/fonts/arial.ttf', 30),
        'font_color': (0, 0, 0),
        'font_selected_color': (255, 0, 0),
    }

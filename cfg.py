WIDTH = 800
HEIGHT = 600
FPS = 60

BG_COLOR = (235, 207, 175)

PLATFORM_EMPTY = '0'
START_POS_PLATFORM = '-1'
PLATFORM_SIZE = (32, 32)
PLATFORM_PARAMS = {
    '1': {'color': (255, 0, 0)},
    '2': {'color': (0, 255, 0)},
    '3': {'color': (0, 0, 255)},
    '4': {'color': (255, 255, 255)},
    '5': {'color': (0, 0, 0)}
}

OBJECTS_PARAMS = {
    '6': {
        'color': (255, 255, 0),
        'form': 'circle',
        'radius': 10
    },
    '8': {
        'color': (255, 0, 255),
        'form': 'rect'
    }
}

ENEMIES_PARAMS = {
    '7': {
        'color': (165, 42, 42),
        'speed_x': 5,
        'direction': 1
    }
}

PLAYER_SIZE = (32, 32)
PLAYER_VELOCITY_X = 5
PLAYER_COLOR = (100, 100, 100)
PLAYER_COLLIDE_RECT_SIZE = (22, 26) # этот прямоугольник будет использоваться для взаимодействия с окружением

GRAVITY = 1
JUMP_POWER = -15
MAX_FALL_SPEED = 15

from .settings import *
from .world import World, Levels


class Game:
    def __init__(self):
        # init
        self.world = None
        self.tmx_maps = None

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

    def load_world(self, level):
        if level == None:
            level = Levels.WORLD_1 #TODO: MENU
        self.world = World(level)

    def run(self):
        while True:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # LOGIC
            pygame.display.update()

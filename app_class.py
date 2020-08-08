import sys

from pygame import event
from settings import *
from buttons import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        # start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # wall node List (includes the coordinate of borders)
        self.wall_node = wall_nodes_coordinate_list.copy()

        # define main-menu buttons
        self.bfs_button = Buttons(
            self, ACIDLIME, 338, MAIN_BUTTON_Y, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, 'Breadth-First Search')
        self.dfs_button = Buttons(
            self, ACIDLIME, 538, MAIN_BUTTON_Y, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, 'Depth-First Search')
        self.astar_button = Buttons(
            self, ACIDLIME, 738, MAIN_BUTTON_Y, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, 'A* search')
        self.dijkstra_button = Buttons(
            self, ACIDLIME, 338, MAIN_BUTTON_Y, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, 'Dijkstra Search')

        # define grid-menu button
        self.start_end_node_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT*2 + GRID_BUTTON_SPACE*2, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.visualize_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT*3 + GRID_BUTTON_SPACE*3, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Vizualize')
        self.main_menu_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT*4 + GRID_BUTTON_SPACE*4, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Main Menu')
        self.exit_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT*5 + GRID_BUTTON_SPACE*5, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, 'Exit')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_menu_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'visualize':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main()

            pygame.quit()
            sys.exit()

######################### SETUP FUNCTIONS #########################

# LOADING IMAGES
    def load(self):
        self.main_menu_background = pygame.image.load('main_background.png')
        self.legends = pygame.image.load('legends.png')

# DRAW TEXT
    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        textimg = font.render(words, True, color)
        text_size = textimg.get_size()
        if centered:
            pos[0] = pos[0] - text_size // 2
            pos[1] = pos[1] - text_size // 2
        screen.blit(textimg, pos)

# SETUP FOR MAIN MENU
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))
        self.bfs_button.draw_buttons(WHITE)
        self.dfs_button.draw_buttons(WHITE)
        self.astar_button.draw_buttons(WHITE)
        self.dijkstra_button.draw_buttons(WHITE)

# SETUP FOR GRID MENU
    def sketch_grid_menu(self):
        self.screen.fill(GRAY)
        self.screen.blit(self.legends, (0, 0))
        self.start_end_node_button.draw_buttons()
        self.wall_node_button.draw_buttons()
        self.reset_button.draw_buttons()
        self.main_menu_button.draw_buttons()
        self.exit_button.draw_buttons()

# DRAW GRID
    def sketch_grid(self):
        pygame.draw.rect(
            self.screen, SPRINGGREEN, (176, 24, GRID_WIDTH, GRID_HEIGHT)
        )
        # there are 45 square pixels across on the grid [without borders!]
        # there are 28 square pixels vertically on the grid [without borders!]
        for x in range(45):
            pygame.draw.line(
                self.screen, WHITE,
                (GS_X + x*self.grid_square_length, GS_Y),
                (GE_X + x*self.grid_square_length, GE_Y)
            )

        for y in range(28):
            pygame.draw.line(
                self.screen, WHITE,
                (GS_X, GS_Y + y*self.grid_square_length),
                (GE_X, GE_Y + y*self.grid_square_length)
            )

# SETUP FOR MAIN MENU BUTTONS
    def main_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bfs_button.is_over(pos):
                self.algorithm_state = 'bfs'
                self.state = 'grid window'
            if self.dfs_button.is_over(pos):
                self.algorithm_state = 'dfs'
                self.state = 'grid window'
            if self.astar_button.is_over(pos):
                self.algorithm_state = 'astar'
                self.state = 'grid window'
            if self.dijkstra_button.is_over(pos):
                self.algorithm_state = 'dijlstra'
                self.state = 'grid window'

        if event.type == pygame.MOUSEMOTION:
            if self.bfs_button.is_over(pos):
                self.bfs_button.color = LEMON
            elif self.dfs_button.is_over(pos):
                self.dfs_button.color = LEMON
            elif self.astar_button.is_over(pos):
                self.astar_button.color = LEMON
            elif self.dijkstra_button.is_over(pos):
                self.dijkstra_button.color = LEMON
            else:
                self.bfs_button.color, self.dfs_button.color, self.astar_button.color, self.dijkstra_button.color = ACIDLIME

# SETUP FOR GRID MENU BUTTONS
    def grid_menu_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.is_over(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.is_over(pos):
                self.state = 'draw walls'
            elif self.reset_button.is_over(pos):
                self.execute_reset()
            elif self.visualize_button.is_over(pos):
                self.state = 'visualize'
            elif self.main_menu_button.is_over(pos):
                self.back_to_main_menu()
            elif self.exit_button.is_over(pos):
                self.exit_app()

        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.is_over(pos):
                self.start_end_node_button.color = MINT
            elif self.wall_node_button.is_over(pos):
                self.wall_node_button.color = MINT
            elif self.reset_button.is_over(pos):
                self.reset_button.color = MINT
            elif self.visualize_button.is_over(pos):
                self.visualize_button.color = MINT
            elif self.main_menu_button.is_over(pos):
                self.main_menu_button.color = MINT
            elif self.exit_button.is_over(pos):
                self.exit_button.color = MINT
            else:
                self.start_end_node_button.color, self.wall_node_button.color, self.reset_button.color, self.visualize_button.color, self.main_menu_button.color, self.exit_button.color = AZURE

    def grid_button_keep_color(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.color = MINT
        if self.state == 'draw walls':
            self.wall_node_button.color = MINT

    def execute_reset(self):
        self.start_end_checker = 0
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        self.wall_node = wall_nodes_coordinate_list.copy()
        self.state = 'grid window'

    def back_to_main_menu(self):
        self.start_end_checker = 0
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        self.wall_node = wall_nodes_coordinate_list.copy()
        self.state = 'main menu'

    def exit_app(self):
        pygame.quit()
        sys.exit()

######################## EXECUTION FUNCTIONS ########################
    def main_menu_events(self):
        # draw background
        pygame.display.update()
        self.sketch_main_menu()
        # check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running == False
            pos = pygame.mouse.getpos()
            self.main_buttons(pos, event)

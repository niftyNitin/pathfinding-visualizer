import sys
from settings import *
from buttons import *
from bfs import *
from dfs import *
from astar import *
from dijkstra import *
from visualize_path import *


class App:
    def __init__(self):
        self.main_menu_background = pygame.image.load('main_background.png')
        self.legends = pygame.image.load('legends.png')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
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
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT + GRID_BUTTON_SPACE, GRID_BUTTON_WIDTH,
            GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT * 2 + GRID_BUTTON_SPACE * 2, GRID_BUTTON_WIDTH,
            GRID_BUTTON_HEIGHT, 'Reset')
        self.visualize_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT * 3 + GRID_BUTTON_SPACE * 3, GRID_BUTTON_WIDTH,
            GRID_BUTTON_HEIGHT, 'Visualize')
        self.main_menu_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT * 4 + GRID_BUTTON_SPACE * 4, GRID_BUTTON_WIDTH,
            GRID_BUTTON_HEIGHT, 'Main Menu')
        self.exit_button = Buttons(
            self, AZURE, 2, GRID_BUTTON_START + GRID_BUTTON_HEIGHT * 5 + GRID_BUTTON_SPACE * 5, GRID_BUTTON_WIDTH,
            GRID_BUTTON_HEIGHT, 'Exit')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'visualize':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main()

            pygame.quit()
            sys.exit()

    ''' SETUP FUNCTIONS '''

    # DRAW TEXT
    @staticmethod
    def draw_text(words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        textimage = font.render(words, True, color)
        text_size = textimage.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(textimage, pos)

    # SETUP FOR MAIN MENU
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))
        self.bfs_button.draw_buttons(WHITE)
        self.dfs_button.draw_buttons(WHITE)
        self.astar_button.draw_buttons(WHITE)
        self.dijkstra_button.draw_buttons(WHITE)

    # SETUP FOR GRID MENU
    def sketch_hotbar(self):
        self.screen.fill(GRAY)
        self.screen.blit(self.legends, (0, 0))

    def sketch_grid_buttons(self):
        self.start_end_node_button.draw_buttons()
        self.wall_node_button.draw_buttons()
        self.reset_button.draw_buttons()
        self.main_menu_button.draw_buttons()
        self.exit_button.draw_buttons()

    # DRAW GRID
    def sketch_grid(self):
        pygame.draw.rect(self.screen, SPRINGGREEN,
                         (176, 24, GRID_WIDTH, GRID_HEIGHT))
        # there are 45 square pixels across on the grid [without borders!]
        # there are 28 square pixels vertically on the grid [without borders!]
        for x in range(45):
            pygame.draw.line(
                self.screen, WHITE,
                (GS_X + x * 24, GS_Y),
                (GS_X + x * 24, GE_Y)
            )

        for y in range(28):
            pygame.draw.line(
                self.screen, WHITE,
                (GS_X, GS_Y + y * 24),
                (GE_X, GS_Y + y * 24)
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
                self.algorithm_state = 'dijkstra'
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
                self.bfs_button.color, self.dfs_button.color, self.astar_button.color, self.dijkstra_button.color = [
                    ACIDLIME, ACIDLIME, ACIDLIME, ACIDLIME]

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
                self.start_end_node_button.color, self.wall_node_button.color, self.reset_button.color, self.visualize_button.color, self.main_menu_button.color, self.exit_button.color = AZURE, AZURE, AZURE, AZURE, AZURE, AZURE

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

    @staticmethod
    def exit_app():
        pygame.quit()
        sys.exit()

    ''' EXECUTION FUNCTIONS '''

    # MAIN MENU FUNCTION
    def main_menu_events(self):
        # draw background
        pygame.display.update()
        self.sketch_main_menu()
        # check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            self.main_buttons(pos, event)

    # PLAY-STATE FUNCTIONS
    def grid_events(self):
        self.sketch_hotbar()
        self.sketch_grid_buttons()
        self.sketch_grid()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # grid button helper function
            self.grid_menu_buttons(pos, event)

    # DRAWING STATE FUNCTIONS
    #  check whether mouse is clicking on the grid
    def draw_nodes(self):
        self.grid_button_keep_color()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.grid_menu_buttons(pos, event)

            # set boundaries for where mouse pointer is valid
            if GS_X < pos[0] < GE_X and GS_Y < pos[1] < GE_Y:
                x_grid_pos = (pos[0] - GS_X) // 24
                y_grid_pos = (pos[1] - GS_Y) // 24
                print('GRID COORDINATE:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if clicking button. Draw if clicking. Check draw state
                if event.type == pygame.MOUSEDOWN:
                    self.mouse_drag = 1

                    # Draw starting and end nodes. Not to be included in the drag feature
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # choose point color for grid and record the coordinate of start pos
                        if self.start_end_checker == 0:
                            node_color = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            self.start_end_checker += 1

                        # choose point color for grid and record the coordinates of end pos
                        # also check that the ned node is not the same as the starting node
                        elif self.start_end_checker == 1 and (x_grid_pos + 1, y_grid_pos + 1) != (
                                self.start_node_x, self.start_node_y):
                            node_color = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            self.start_end_checker += 1

                        else:
                            continue

                        # draw point on grid
                        pygame.draw.rect(
                            self.screen, node_color, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEUP:
                    self.mouse_drag = 0

                # check if mouse is being dragged
                if self.mouse_drag == 1:
                    # draw wall node and append wall node coordinates to the wall node list
                    # check if wall node being drawn/added is already in the list
                    # check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_node \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            pygame.draw.rect(
                                self.screen, BLACK, (GS_X + x_grid_pos * 24, GS_Y + y_grid_pos * 24, 24, 24))
                            self.wall_node.append(
                                (x_grid_pos + 1, y_grid_pos + 1))

    ''' VISUALIZATION FUNCTIONS '''

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # BFS
        if self.algorithm_state == 'bfs':
            self.bfs = breadth_first(self, self.start_node_x, self.start_node_y,
                                     self.end_node_x, self.end_node_y, self.wall_node)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # Make object for new path
            if self.bfs.route_found:
                self.draw_path = visualize_path(self.screen, self.start_node_x,
                                                self.start_node_y, self.bfs.route, [])

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen,
                               (640, 360), 48, RED, FONT, centered=True)

        # DFS
        elif self.algorithm_state == 'dfs':
            self.dfs = depth_first(self, self.start_node_x, self.start_node_y,
                                   self.end_node_x, self.end_node_y, self.wall_node)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            # Make object for new path
            if self.dfs.route_found:
                self.draw_path = visualize_path(self.screen, self.start_node_x,
                                                self.start_node_y, self.dfs.route, [])

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen,
                               (640, 360), 48, RED, FONT, centered=True)

        # A-STAR
        elif self.algorithm_state == 'astar':
            self.astar = astar(self, self.start_node_x, self.start_node_y,
                               self.end_node_x, self.end_node_y, self.wall_node)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            # Make object for new path
            if self.astar.route_found:
                self.draw_path = visualize_path(self.screen, self.start_node_x,
                                                self.start_node_y, self.astar.route, [])

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen,
                               (640, 360), 48, RED, FONT, centered=True)

        # DIJKSTRA
        elif self.algorithm_state == 'dijkstra':
            self.dijkstra = dijkstra(self, self.start_node_x, self.start_node_y,
                                     self.end_node_x, self.end_node_y, self.wall_node)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.astar_execute()

            # Make object for new path
            if self.dijkstra.route_found:
                self.draw_path = visualize_path(self.screen, self.start_node_x,
                                                self.start_node_y, self.dijkstra.route, [])

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen,
                               (640, 360), 48, RED, FONT, True)

        pygame.display.update()
        self.state = 'aftermath'

    ''' AFTERMATH FUNCTIONS '''

    def reset_or_main(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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
                    self.start_end_node_button.color, self.wall_node_button.color, self.reset_button.color, self.visualize_button.color, self.main_menu_button.color, self.exit_button.color = AZURE, AZURE, AZURE, AZURE, AZURE, AZURE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.is_over(pos):
                    self.execute_reset()
                elif self.main_menu_button.is_over(pos):
                    self.back_to_main_menu()

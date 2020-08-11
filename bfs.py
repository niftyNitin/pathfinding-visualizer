import collections
from settings import *

class breadth_first():
	def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
		self.app = app
		self.start_node_x = start_node_x
		self.start_node_y = start_node_y
		self.end_node_x = end_node_x
		self.end_node_y = end_node_y
		self.wall_pos = wall_pos
		self.visited = [(start_node_x, start_node_y)]
		self.route = None
		self.route_found = False

	def draw_all_paths(self, i, j):
		# Draw each node as the algorithm is visiting simultaneously.
		pygame.draw.rect(self.app.screen, TAN, (i*24 + GS_X, j*24 + GS_Y, 24, 24), 0)

		# Redraw start and end nodes on top of all routes
		pygame.draw.rect(self.app.screen, TOMATO, (GS_X + self.start_node_x * 24, GS_Y + self.start_node_y * 24, 24, 24), 0)

		# Redraw grids
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

        pygame.display.update()

    def check_valid(self, move):
    	if move not in self.wall_pos and move not in self.visited:
    		self.visited.append(move)
    		return True
    	return False

    def find_end(self, first_out):
    	if first_out == (self.end_node_x, self.end_node_y):
    		return True
    	return False

    def bfs_execute(self):
    	queue = collections.deque([(self.start_node_x, self.start_node_y)])
    	moves_queue = collections.deque([''])
    	first_out = ''
    	first_moves = ''

    	while queue:
    		# Parent variables of parent nodes at the given time
    		first_out = queue.popleft()
    		first_moves = moves_queue.popleft()
    		for m in ['L', 'R', 'U', 'D']:
    			i, j = first_out
    			if m == 'L':
    				i -= 1
    			elif m == 'R':
    				i += 1
    			elif m == 'U':
    				j -= 1
    			elif m == 'D':
    				j += 1

				# Make new variable "latest_moves" for adding onto the queue again
				# You don't want the 'parent' variable to change
				latest_moves = first_moves + m
				if self.check_valid(i, j):
					self.draw_all_paths(i, j)
					queue.append((i, j))
					moves_queue.append(latest_moves)

				if self.find_end((i, j)):
					self.route = latest_moves
					self.route_found = True
					break

			if self.route_found:
				break




class MazeSolverRecursive(object):

	def __init__(self, maze_def_filename, maze_solution_filename):
		self.loadMaze(maze_def_filename)
		self.maze_solution_filename = maze_solution_filename
		self.maze_constructs = {'wall': '#', 'open': '_', 'start':'s', 'end':'e', 'bad':'!','good':'*'}
		self.path_identifiers = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
		self.deriveStartingCoordinates()
		self.deriveEndingCoordinates()
		self.maze[self.end_row][self.end_col] = self.maze_constructs['end']


	def solve(self):
		self.findPath(self.start_row, self.start_col)
		self.saveResults()
		
		
	def findPath(self, x, y):
		if self.isOutOfBounds(x,y): return False
		elif self.maze[x][y] == self.maze_constructs['end']: return True
		elif self.maze[x][y] == self.maze_constructs['wall']: return False
		self.maze[x][y] = self.maze_constructs['good'] # mark this as a good point on the path to the finish
		if self.findPath(x, y - 1): return True # check up from the current position
		if self.findPath(x + 1, y): return True # check right of the current position
		if self.findPath(x, y + 1): return True # check below current position 
		if self.findPath(x - 1, y): return True # check to the left of current position 
		self.maze[x][y] = self.maze_constructs['bad']
		return False

			
	def notWallOrBadCell(self, x, y):
		if self.isOutOfBounds(x, y) == False:
			if self.maze[x][y] == self.maze_constructs['wall']:
				return False
			elif self.maze[x][y] == self.maze_constructs['bad']:
				return False
			else:
				return True
		else: return True


	def isOutOfBounds(self, x, y):
		if x < 0 or y < 0 or x > self.end_row or y > (len(self.maze[0])) - 1: ## loop 
			return True
		else:
			return False


	def deriveStartingCoordinates(self):
		self.start_row = 0
		self.start_col = self.maze[0].index('_')


	def deriveEndingCoordinates(self):
		self.end_row = len(self.maze) -1
		self.end_col = self.maze[self.end_row].index('_')
		

	def loadMaze(self, maze_def_filename):
		#TODO: add some validation
		maze_def_txt = open(maze_def_filename)
		self.maze = []
		for line in maze_def_txt:
			row = []
			for char in line:
				row.append(char)
			self.maze.append(row)


	def saveResults(self):
		solutions_file = open(self.maze_solution_filename, 'w')
		for chars in self.maze:
			row = ''.join(chars)
			print row.rstrip()
			solutions_file.write(row)
		solutions_file.close()			


			
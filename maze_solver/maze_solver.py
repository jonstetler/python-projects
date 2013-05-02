class MazeSolver(object):

	def __init__(self, maze_def_filename, maze_solution_filename):
		self.loadMaze(maze_def_filename)
		self.maze_solution_filename = maze_solution_filename
		self.maze_constructs = {'wall': '#', 'isopen': '_'}
		self.path_identifiers = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
		self.deriveStartingCoordinates()
		self.deriveEndingCoordinates()

	def solve(self):
		self.findPath(self.start_row, self.start_col)
		self.saveResults()

	def findPath(self, row, col, from_row = 0, from_col = 0):
		if row == self.end_row and col == self.start_row:
			print 'found the end'
			#self.maze[row][col] = "*"
		elif row == self.start_row and col == self.start_col:
			self.maze[self.start_row][self.start_col] = '*'
			self.findPath(row + 1, col)
		elif self.maze[row][col] == self.maze_constructs['isopen']:
			self.maze[row][col] = '*'
			self.findPath(row, col - 1)
		elif self.maze[row][col] == self.maze_constructs['wall']:
			self.findPath(row, col + 1, row, col)
			print "hit a wall...backup"
		elif self.maze[row][col] == '*':
			self.rotate(row, col, from_row, from_col)
			print "backup from [%s,%s]" % (from_row, from_col)
		else:
			print "missing case..at: [%s,%s]" % (row, col)
		
	def rotate(self, row, col, from_row, from_col):
		if row == from_row and col > from_col:
			print "moving down to "
			self.findPath(row + 1, col)
		elif row < row_from and col == from_col:
			self.findPath(row - 1, col)
		else:
			print "got nothing"

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


			
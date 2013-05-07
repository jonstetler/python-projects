class MazeSolver(object):


	def __init__(self, maze_def_filename, maze_solution_filename):
		self.loadMaze(maze_def_filename)
		if self.canSolveMaze:
			self.maze_solution_filename = maze_solution_filename
			self.maze_constructs = {'wall': '#', 'open': '_', 'end':'$', 'bad':'!','good':'+'}
			self.path_identifiers = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
			self.maze[self.end_row][self.end_col] = self.maze_constructs['end']
			self.path_identifier_index = 0


	def solve(self):
		if self.canSolveMaze == True:
			self.find_path(self.start_row, self.start_col)
			self.cleanUpBadCells()
			self.saveResults()


	def find_path(self, row, col):
		while (True):
			if self.isEnd(row, col):
				self.maze[row][col] = self.getNextPathIdentifier()
				break
			elif self.isOpen(row, col):
				self.maze[row][col] = self.getNextPathIdentifier()
			#move to next open space
			elif self.isValidOpenMove(row, col - 1): 
				col -= 1 # move left
			elif self.isValidOpenMove(row + 1, col):
				row += 1 # move down
			elif self.isValidOpenMove(row, col + 1):
				col += 1 # move right
			elif self.isValidOpenMove(row -1, col):
				row -= 1 # move up
			#no open spaces, so backtrack
			elif self.isValidBackTrackMove(row, col + 1): 
				self.markCurrentCellAsBad(row, col)
				col += 1 # move right
			elif self.isValidBackTrackMove(row - 1, col):
				self.markCurrentCellAsBad(row, col)
				row -= 1 # move up
			elif self.isValidBackTrackMove(row, col - 1):
				self.markCurrentCellAsBad(row, col)				
				col -= 1 # move left
			elif self.isValidBackTrackMove(row + 1, col):
				self.markCurrentCellAsBad(row, col)
				row += 1 # move down	
		
	
	def markCurrentCellAsBad(self, row, col): 
		if self.path_identifier_index > 0:
			self.path_identifier_index -= 1
		self.maze[row][col] = self.maze_constructs['bad']
		

	def isOpen(self, row, col):
		if self.maze[row][col] == self.maze_constructs['open']:
			return True
		else:
			return False


	def isEnd(self, row, col):
		if self.maze[row][col] == self.maze_constructs['end']:
			return True
		else:
			return False


	def isValidOpenMove(self, row, col):
		if (not self.isOutOfBounds(row, col) 
			and self.notWallOrBadCell(row, col)
			and not self.isPathIdentifier(row, col)):
			return True
		else: 
			return False


	def isValidBackTrackMove(self, row, col):
		if (self.isOutOfBounds(row, col) == False 
			and self.notWallOrBadCell(row, col) == True):
			return True
		else:
			return False


	def notWallOrBadCell(self, row, col):
		if self.isOutOfBounds(row, col) == False:
			if self.maze[row][col] == self.maze_constructs['wall']:
				return False
			elif self.maze[row][col] == self.maze_constructs['bad']:
				return False
			else:
				return True
		else: return True


	def getNextPathIdentifier(self):
		next_path_identifier = self.path_identifier_index
		while(next_path_identifier >= 26):
			next_path_identifier -= 26
		self.path_identifier_index += 1
		print next_path_identifier
		return self.path_identifiers[next_path_identifier]


	def isPathIdentifier(self, row, col):
		return any(self.maze[row][col].lower() == val.lower() for val in self.path_identifiers)
		

	def isOutOfBounds(self, row, col):
		if row < 0 or col < 0 or row > self.end_row or col > (len(self.maze[0])) - 1: 
			return True
		else:
			return False


	def deriveStartingCoordinates(self):
		self.start_row = 0
		try:
			self.start_col = self.maze[0].index('_')
		except:
			print "ERROR: no starting point defined in maze definition"
			self.canSolveMaze = False


	def deriveEndingCoordinates(self):
		try:
			self.end_row = len(self.maze) -1
			self.end_col = self.maze[self.end_row].index('_')
		except:
			print "ERROR: no ending point defined in maze definition"
			self.canSolveMaze = False


	def loadMaze(self, maze_def_filename):
		self.canSolveMaze = True
		maze_def_txt = open(maze_def_filename)
		self.maze = []
		for line in maze_def_txt:
			row = []
			for char in line:
				row.append(char)
			self.maze.append(row)
		maze_def_txt.close()
		self.deriveStartingCoordinates()
		self.deriveEndingCoordinates()


	def cleanUpBadCells(self):
		row = 0
		for line in self.maze:
			col = 0
			for char in line:
				if char == self.maze_constructs['bad']:
					self.maze[row][col] = '_'
				col += 1
			row += 1


	def saveResults(self):
		solutions_file = open(self.maze_solution_filename, 'w')
		for chars in self.maze:
			row = ''.join(chars)
			print row.rstrip()
			solutions_file.write(row)
		solutions_file.close()	



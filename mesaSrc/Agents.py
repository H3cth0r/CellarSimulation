import mesa as ms
from math import sqrt

# Creating agent for representing the Shelves 
class ShelveAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t
		
class StackAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t

# Agent for recollection object
class ObjectAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t

# Negotiator Agent
class NegotiatorAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t
		self.speed 	=	1
		self.stage  = 	0
		self.counter=	0

	def move(self):
		boxes = self.model.grid.get_neighbors(self.pos, True, False, 1)
		moveOrNot = True
		for i in boxes:
			Box = isinstance(i, ObjectAgent)
			if(Box == True):
				moveOrNot = False
		
		if (moveOrNot == True):
			if (((self.pos[0] == 0) and (self.pos[1] == 0)) or (self.stage == 4)):
				self.stage = 4
				if (self.pos[1] < 10):
					newpos = (self.pos[0], self.pos[1] + self.speed)
					self.model.grid.move_agent(self, newpos)
				else:
					self.stage = 0
			else:
				if (self.stage == 0):
					if(self.pos[0] < 15):
						newpos = (self.pos[0] + self.speed, self.pos[1])
						self.model.grid.move_agent(self, newpos)
						if(self.pos[0] == 15):
							self.stage = 1
				elif (self.stage == 1):
					if(self.counter < 2):
						self.counter += 1
						newpos = (self.pos[0], self.pos[1] - self.speed)
						self.model.grid.move_agent(self, newpos)
						if(self.counter == 2):
							print(self.counter)
							self.stage = 2
							self.counter = 0
				elif (self.stage == 2):
					if(self.pos[0] > 0):
						newpos = (self.pos[0] - self.speed, self.pos[1])
						self.model.grid.move_agent(self, newpos)
						if(self.pos[0] == 0):
							self.stage = 3
				elif (self.stage == 3):
					if(self.counter < 2):
						self.counter += 1
						newpos = (self.pos[0], self.pos[1] - self.speed)
						self.model.grid.move_agent(self, newpos)
						if(self.counter == 2):
							self.stage = 0
							self.counter = 0
							print(self.pos)
	
	def stage_one(self):
		pass

	def stage_two(self):
		self.move()
	
# Agent Robot Agent
class RobotAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t
		self.busy   =   0
		self.destination = None
		self.direction = 0
		self.prev = 0 # 0 = up, 1 = down, 2 = left, 3 = right
	
	def offerContract(self, box):
		if self.busy == 1:
			return -1
		else:
			return sqrt((box.pos[0] - self.pos[0])^2 + (box.pos[1] - self.pos[1])^2)

	def signContract(self, dest):
		self.destination = dest

	def move(self):
		if self.destination == None:
			return
		
		dx = self.destination[0] - self.pos[0]
		dy = self.destination[1] - self.pos[1]

		directions = []
		if dx == 0 and dy == 0:
			# arrived at destination
			return
		elif dx == 0:
			if dy > 0:
				directions = [0, 3, 2, 1]
			else:
				directions = [1, 2, 3, 0]
		elif dy == 0:
			if dx > 0:
				directions = [3, 1, 0, 2]
			else:
				directions = [2, 0, 1, 3]
		elif dx > 0 and dy > 0:
			if abs(dx) <= abs(dy):
				directions = [3, 0, 2, 1]
			else:
				directions = [0, 3, 1, 2]
		elif dx < 0 and dy > 0:
			if abs(dx) <= abs(dy):
				directions = [2, 0, 3, 1]
			else:
				directions = [0, 2, 1, 3]
		elif dx < 0 and dy < 0:
			if abs(dx) <= abs(dy):
				directions = [2, 1, 3, 0]
			else:
				directions = [1, 2, 0, 3]
		else:
			if abs(dx) <= abs(dy):
				directions = [3, 1, 2, 0]
			else:
				directions = [1, 3, 0, 2]
		

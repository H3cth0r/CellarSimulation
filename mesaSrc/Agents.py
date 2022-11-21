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
		

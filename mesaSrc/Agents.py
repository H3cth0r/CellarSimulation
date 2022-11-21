import mesa as ms


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
	
	

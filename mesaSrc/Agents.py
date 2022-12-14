import mesa as ms
from random import choice, randrange
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
		self.stackSize = 0

# Agent for recollection object
class ObjectAgent(ms.Agent):
	def __init__(self, id_t, model):
		super().__init__(id_t, model)
		self.id		=	id_t
		

# Negotiator Agent
class NegotiatorAgent(ms.Agent):
	def __init__(self, id_t, model, robots):
		super().__init__(id_t, model)
		self.id	= id_t
		self.speed = 1
		self.stage = 0
		self.counter = 0
		self.robots = robots
		self.dispatchedBoxes = []
		self.creatingContract = False
		self.energyUsed = 	0

	def createContract(self, box):
		if box.unique_id in self.dispatchedBoxes:
			return False

		minDist = 10000
		luckyRobot = None
		for robot in self.robots:
			toCompare = robot.offerContract(box)
			if toCompare >= 0 and toCompare < minDist:
				minDist = toCompare
				luckyRobot = robot
		
		if luckyRobot != None:
			luckyRobot.signContract(box.pos)
			self.dispatchedBoxes.append(box.unique_id)
		return True

	def move(self):
		agents = self.model.grid.get_neighbors(self.pos, True, False, 1)
		self.creatingContract = False
		for obj in agents:
			boxFound = isinstance(obj, ObjectAgent)
			if boxFound:
				self.creatingContract = self.createContract(obj)
		
		if not self.creatingContract:
			if (((self.pos[0] == 0) and (self.pos[1] == 0)) or (self.stage == 4)):
				self.stage = 4
				if (self.pos[1] < 10):
					newpos = (self.pos[0], self.pos[1] + self.speed)
					self.model.grid.move_agent(self, newpos)
					self.energyUsed += 1
				else:
					self.stage = 0
			else:
				if (self.stage == 0):
					if(self.pos[0] < 15):
						newpos = (self.pos[0] + self.speed, self.pos[1])
						self.model.grid.move_agent(self, newpos)
						self.energyUsed += 1
						if(self.pos[0] == 15):
							self.stage = 1
				elif (self.stage == 1):
					if(self.counter < 2):
						self.counter += 1
						newpos = (self.pos[0], self.pos[1] - self.speed)
						self.model.grid.move_agent(self, newpos)
						self.energyUsed += 1
						if(self.counter == 2):
							#print(self.counter)
							self.stage = 2
							self.counter = 0
				elif (self.stage == 2):
					if(self.pos[0] > 0):
						newpos = (self.pos[0] - self.speed, self.pos[1])
						self.model.grid.move_agent(self, newpos)
						self.energyUsed += 1
						if(self.pos[0] == 0):
							self.stage = 3
				elif (self.stage == 3):
					if(self.counter < 2):
						self.counter += 1
						newpos = (self.pos[0], self.pos[1] - self.speed)
						self.model.grid.move_agent(self, newpos)
						self.energyUsed += 1
						if(self.counter == 2):
							self.stage = 0
							self.counter = 0
							#print(self.pos)
	
	def stage_one(self):
		pass

	def stage_two(self):
		self.move()

# Agent Random Robot Agent
class RandomRobotAgent(ms.Agent):
	def __init__(self, id_t, model, stacks):
		super().__init__(id_t, model)
		self.id 		= 	id_t
		self.busy 		=	True
		self.prev 		=	(0, 0)
		self.carrying	=	False
		self.energyUsed = 	0

	def checkforagent(self):
		#directions = self.model.grid.get_neighborhood(self.pos, False, False, 1)
		neighborAgent = self.model.grid.get_neighbors(self.pos, False, False, 1)
		for i in neighborAgent:
			if isinstance(i, ObjectAgent) and not self.carrying:
				self.carrying = True
				self.prev = (0, 0)
				self.model.grid.remove_agent(i)
			elif isinstance(i, StackAgent) and self.carrying:
				self.carrying = False
				self.prev = (0, 0)
			else:
				continue
			
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		if self.prev != (0,0):
			print(self.prev)
			directions.remove((self.prev[0]*-1, self.prev[1]*-1))
		while(len(directions) > 0):
			randomDir = randrange(0, len(directions))
			dir = directions[randomDir]
			directions.remove(dir)
			newPos = self.pos[0] + dir[0], self.pos[1] + dir[1]
			if (newPos[0] < 0 or newPos[1] < 0) or (newPos[0] >= self.model.grid.width or newPos[1] >= self.model.grid.height):
				continue
			obstacles = self.model.grid.get_cell_list_contents(newPos)
			validDir = True
			for obs in obstacles:
				if not isinstance(obs, ObjectAgent):
					validDir = False
			if validDir:
				self.prev = dir
				return newPos
		newPos = self.pos[0] + self.prev[0], self.pos[1] + self.prev[1]
		if (newPos[0] < 0 or newPos[1] < 0) or (newPos[0] >= self.model.grid.width or newPos[1] >= self.model.grid.height):
			return None
		obstacles = self.model.grid.get_cell_list_contents(newPos)
		validDir = True
		for obs in obstacles:
			if not isinstance(obs, ObjectAgent):
				validDir = False
		if validDir:
			return newPos
		return None
			
	def move(self):
		newdir = self.checkforagent()
		if (newdir != None):
			self.model.grid.move_agent(self, newdir)
			self.energyUsed += 1
		
		

	def stage_one(self):
		pass

	def stage_two(self):
		self.move()


	
# Agent Robot Agent
class RobotAgent(ms.Agent):
	def __init__(self, id_t, model, stacks):
		super().__init__(id_t, model)
		self.id		=	id_t
		self.busy   =   False
		self.destination = None
		self.direction = 0
		self.prev = -1 # 0 = up, 1 = down, 2 = left, 3 = right
		self.conflictedWith = -1
		self.carrying = False
		self.stacks = stacks
		self.energyUsed = 	0
	
	def offerContract(self, box):
		if self.busy or self.carrying:
			return -1
		else:
			return sqrt((box.pos[0] - self.pos[0])**2 + (box.pos[1] - self.pos[1])**2)

	def signContract(self, dest):
		self.destination = dest
		self.busy = True

	def nearestStack(self):
		minDist = 10000
		nearestStackPos = (-1, -1)
		for stack in self.stacks:
			prevSqrt = (stack.pos[0] - self.pos[0])**2 + (stack.pos[1] - self.pos[1])**2
			#print(f"prev to sqrt: {prevSqrt}")
			toCompare = sqrt((stack.pos[0] - self.pos[0])**2 + (stack.pos[1] - self.pos[1])**2)
			if toCompare < minDist:
				nearestStackPos = stack.pos
				minDist = toCompare
		return nearestStackPos

	def move(self):
		if self.destination == None:
			return
		
		#print(f"Searching for movements for robot {self.unique_id}")
		dx = self.destination[0] - self.pos[0]
		dy = self.destination[1] - self.pos[1]

		directions = []
		if dx == 0 and dy == 0:
			# arrived at destination
			obstacles = self.model.grid.get_cell_list_contents(self.pos)
			for obstacle in obstacles:
				if isinstance(obstacle, ObjectAgent):
					# grab the box
					self.carrying = True
					self.prev = -1
					self.model.grid.remove_agent(obstacle) ### CHANGE TO METHOD
					# look for nearest stack
					self.destination = self.nearestStack()
					return
			directions = [0, 1, 2, 3]
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
				directions = [0, 3, 2, 1]
			else:
				directions = [3, 0, 1, 2]
		elif dx < 0 and dy > 0:
			if abs(dx) <= abs(dy):
				directions = [0, 2, 3, 1]
			else:
				directions = [2, 0, 1, 3]
		elif dx < 0 and dy < 0:
			if abs(dx) <= abs(dy):
				directions = [1, 2, 3, 0]
			else:
				directions = [2, 1, 0, 3]
		else:
			if abs(dx) <= abs(dy):
				directions = [1, 3, 2, 0]
			else:
				directions = [3, 1, 0, 2]
		
		dirToVec = {
			0: [ 0,  1],
			1: [ 0, -1],
			2: [-1,  0],
			3: [ 1,  0]
		}
		prevDict = {
			0: 1,
			1: 0,
			2: 3,
			3: 2
		}
		newPos = (-1, -1)
		self.conflictedWith = -1
		tryAgain = True
		while tryAgain:
			#print(f"directions: {directions}")
			for direction in directions:
				#print(f"Trying direction {direction}")
				if direction == self.prev and len(directions) > 1:
					"""
					if direction == self.prev:
						print(f"Direction {direction} is prev")
					"""
					continue
				v = dirToVec[direction]
				newPos = (self.pos[0] + v[0], self.pos[1] + v[1])
				newDir = direction
				newPosIsValid = True
				if (newPos[0] < 0 or newPos[1] < 0) or (newPos[0] >= self.model.grid.width or newPos[1] >= self.model.grid.height):
					#print(f"Direction {direction} is out of bounds")
					newPosIsValid = False
					continue
				obstacles = self.model.grid.get_cell_list_contents(newPos)
				
				for obstacle in obstacles:
					#print(f"When trying to move to direction {direction}, object {obstacle} was found")
					if isinstance(obstacle, ObjectAgent):
						# check if it's the box i was sent to carry
						if self.destination == obstacle.pos:
							# grab the box
							self.carrying = True
							self.prev = -1
							self.model.grid.remove_agent(obstacle) ### CHANGE TO METHOD
							# look for nearest stack
							self.destination = self.nearestStack()
							return
						else:
							#ignore box
							continue
					if isinstance(obstacle, RobotAgent):
						#print(f"Obstacle was robot {obstacle.unique_id}")
						if (obstacle.conflictedWith == self.unique_id) or (not obstacle.busy):
							"""
							if obstacle.conflictedWith == self.unique_id:
								print(f"Robot obstacle was conflicted with me")
							elif not obstacle.busy:
								print(f"Robot obstacle was not busy")
							"""
							# if robot obstacle is already conflicted with me or if it's not active,
							# i should continue to look for another place to move
							newPosIsValid = False
							break
						else:
							# if robot obstacle is not conflicted with me, i should wait and see if
							# it moves the next step
							self.conflictedWith = obstacle.unique_id
							return
					elif isinstance(obstacle, StackAgent) and self.carrying:
						# stack was found, so i deliver the box and deactivate
						obstacle.stackSize += 1 ### CHANGE TO METHOD
						self.carrying = False
						self.destination = None
						self.busy = False
						self.prev = -1
						return
					else:
						# obstacle wasn't a robot, so i should continue to look for another place to 
						# move
						newPosIsValid = False
						break

				#print(f"Out of for")
				#print(f"new pos is valid: {newPosIsValid}")	
				if newPosIsValid:

					# if newPose is valid, we don't need to look for somewhere else to move
					break
			if self.prev != -1 and not newPosIsValid: 
				directions = [self.prev]
				tryAgain = 1
				self.prev = -1
			else:
				tryAgain = False
		
		#print(f"Moving to: {newPos}")
		if newPos[0] != -1:
			self.model.grid.move_agent(self, newPos)
			self.prev = prevDict[newDir]
			self.energyUsed += 1
		"""
		else:
			#print(f"No valid directions for robot {self.unique_id}")
		"""
	def stage_one(self):
		pass

	def stage_two(self):
		self.move()
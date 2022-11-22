import mesa as ms
from Agents import ShelveAgent, ObjectAgent, NegotiatorAgent, RobotAgent, StackAgent

def something(model):
	return 1

def getDeactivatedRobots(model):
    return sum([1 for agent in model.schedule.agents if isinstance(agent, RobotAgent) and not agent.busy])

def getRemainingBoxes(model):
	return sum([1 for agent in model.boxList if isinstance(agent, ObjectAgent) and agent.pos != None])

class CellarModel(ms.Model):
	def __init__(self, nBoxes):
		super().__init__()

		# Configuration of stages & schedule
		self.model_stages	=	["stage_one", "stage_two"]
		self.schedule		=	ms.time.StagedActivation(self, self.model_stages, shuffle=False)

		# Configuration of Grid
		self.grid		=	ms.space.MultiGrid(16, 11, torus=False)
		self.direction		=	[
					[1,  0],
					[0,  1],
					[-1, 0],
					[0, -1]
		]
		self.datacollector = ms.DataCollector(
			model_reporters = {
				"Deactivated Robots" : getDeactivatedRobots,
				"Remaining Boxes" : getRemainingBoxes
				}
		)
		
		# adding stacks
		points_stacks = [(4, 3), (11, 3), (4, 7), (11, 7)]
		stackList = []
		for i in points_stacks:
			SA = StackAgent(i[0], self)
			stackList.append(SA)
			self.grid.place_agent(SA, i)

		points_stacks += [(3, 3), (12, 3), (3, 7), (12, 7)]
		# adding shelves
		input_row = False
		for y in range(11):
			if input_row == True:
				shelves = [(1, y),  (2, y),  (3, y),  (4, y), 
				       (6, y),  (7, y),  (8, y),  (9, y),
				       (11, y), (12, y), (13, y), (14, y)
				]
				for x in shelves:
					
					if x not in points_stacks:
						#print(f"Adding shelve: {x}")
						SA = ShelveAgent(x[0], self)
						self.grid.place_agent(SA, x)	
				input_row = False
				continue
			input_row = True

		# adding robots
		points_robots = [(4, 2), (11, 2), (4, 8), (11, 8)]
		robot_list = []
		for i in points_robots:
			RA = RobotAgent(self.next_id(), self, stackList)
			robot_list.append(RA)
			self.schedule.add(RA)
			self.grid.place_agent(RA, i)
		
		# adding negotiators
		points_neg = [(0, 10)]
		for i in points_neg:
			NA = NegotiatorAgent(self.next_id(), self, robot_list)
			self.schedule.add(NA)
			self.grid.place_agent(NA, i)

		self.boxList = []
		for i in range(nBoxes):
			OA = ObjectAgent(self.next_id(), self)
			self.grid.place_agent(OA, self.grid.find_empty())
			self.boxList.append(OA)
		"""
		RA = RobotAgent(self.next_id(), self, stackList)
		RA.signContract((15, 7))
		self.schedule.add(RA)
		self.grid.place_agent(RA, (1, 2))

		RA = RobotAgent(self.next_id(), self, stackList)
		RA.signContract((2, 6))
		self.schedule.add(RA)
		self.grid.place_agent(RA, (14, 2))
		
		# adding boxes
		OA = ObjectAgent(self.next_id(), self)
		self.grid.place_agent(OA, (15, 7))

		OA = ObjectAgent(self.next_id(), self)
		self.grid.place_agent(OA, (2, 6))
		"""
	def step(self):
		self.datacollector.collect(self)
		self.schedule.step()
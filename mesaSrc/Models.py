import mesa as ms
from Agents import ShelveAgent, ObjectAgent, NegotiatorAgent, RobotAgent, StackAgent

def something(model):
	return 1

class CellarModel(ms.Model):
	def __init__(self):
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
			model_reporters={"something"	:	something}
		)

		# adding shelves
		input_row = False
		for y in range(11):
			if input_row == True:
				shelves = [(1, y),  (2, y),  (3, y),  (4, y), 
				       (6, y),  (7, y),  (8, y),  (9, y),
				       (11, y), (12, y), (13, y), (14, y)
				]
				for x in shelves:
					SA = ShelveAgent(x[0], self)
					self.grid.place_agent(SA, x)	
				input_row = False
				continue
			input_row = True
		
		# adding stacks
		points_stacks = [(4, 3), (11, 3), (4, 7), (11, 7)]
		stackList = []
		for i in points_stacks:
			SA = StackAgent(i[0], self)
			stackList.append(SA)
			self.grid.place_agent(SA, i)

		# adding negotiators
		points_neg = [(0, 10)]
		for i in points_neg:
			NA = NegotiatorAgent(self.next_id(), self)
			self.schedule.add(NA)
			self.grid.place_agent(NA, i)

		# adding robots
		points_robots = [(1, 2), (8, 2)]
		for i in points_robots:
			RA = RobotAgent(self.next_id(), self)
			RA.destination = (5, 9)
			RA.busy = True
			RA.stacks = stackList
			self.schedule.add(RA)
			self.grid.place_agent(RA, i)

	def step(self):
		self.schedule.step()
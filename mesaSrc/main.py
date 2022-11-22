import mesa as ms
from Models import *
from Agents import *


def agent_PT(agent):
	if type(agent) == ShelveAgent:
		PT = {"Shape": "rect","Color": "grey","Filled": "true","Layer": 1,"w": 1,"h":1}
	elif type(agent) == StackAgent:
		PT = {"Shape": "rect","Color": "#E8D33F","Filled": "true","Layer": 0,"w": 1,"h":1}
	elif type(agent) == RobotAgent:
		if agent.busy:
			if agent.carrying:
				PT = {"Shape": "circle","Color": "#3772FF","Filled": "true","Layer": 0, "r": 1}
			else:
				PT = {"Shape": "circle","Color": "#093A3E","Filled": "true","Layer": 0, "r": 1}
		else:
			PT = {"Shape": "circle","Color": "#001011","Filled": "true","Layer": 0, "r": 1}
	elif type(agent) == NegotiatorAgent:
		if agent.creatingContract:
			PT = {"Shape": "circle", "Color": "#FB8B24", "Filled": "true", "Layer": 4, "r": 0.8}
		else:
			PT = {"Shape": "circle", "Color": "#1D201F", "Filled": "true", "Layer": 4, "r": 0.8}
	elif type(agent) == ObjectAgent:
		PT = {"Shape": "rect", "Color": "#8C705F", "Filled": "true", "Layer": 3, "w": 0.8,"h":0.8}
	else:
		PT = {"Shape": "rect","Color": "red","Filled": "true","Layer": 0,"w": 1,"h":1}
	return PT

grid	=	ms.visualization.CanvasGrid(agent_PT, 16, 11, 600, 400)

chart_currents	=	ms.visualization.ChartModule(
	[],
	canvas_height	= 300,
	data_collector_name	= "datacollector"
)

server		=	ms.visualization.ModularServer(CellarModel, [grid, chart_currents], "Cellar Model", {"nBoxes":12})
server.port	= 8521
server.launch()

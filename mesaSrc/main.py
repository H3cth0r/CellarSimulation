import mesa as ms
from Models import *
from Agents import *


def agent_PT(agent):
	if type(agent) == ShelveAgent:
		PT = {"Shape": "rect","Color": "grey","Filled": "true","Layer": 0,"w": 1,"h":1}
	elif type(agent) == StackAgent:
		PT = {"Shape": "rect","Color": "blue","Filled": "true","Layer": 0,"w": 1,"h":1}
	elif type(agent) == NegotiatorAgent:
		PT = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 0, "r": 1}
	else:
		PT = {"Shape": "rect","Color": "red","Filled": "true","Layer": 0,"w": 1,"h":1}
	return PT


grid	=	ms.visualization.CanvasGrid(agent_PT, 16, 11, 600, 400)

chart_currents	=	ms.visualization.ChartModule(
	[],
	canvas_height	= 300,
	data_collector_name	= "datacollector"
)

server		=	ms.visualization.ModularServer(CellarModel, [grid, chart_currents], "Cellar Model", {})
server.port	= 8521
server.launch()

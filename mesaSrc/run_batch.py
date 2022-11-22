import mesa as ms
from Models import *
from Agents import *
import pandas as pd
import matplotlib.pyplot as plt

params = {"nBoxes":12}
results = ms.batch_run(
    CellarModel,
    parameters=params,
    iterations=3,
    max_steps=125,
    number_processes=1,
    data_collection_period=1,
    display_progress=True)


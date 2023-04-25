import EVRP
import numpy as np
from time import sleep
import os
import settings

points = np.random.randint(1, 101, size=(20 + 1, 2))
charger = np.random.randint(1, 101, size=(3, 2))
os.system('cls' if os.name == 'nt' else 'clear')

config:settings.config = settings.config

config.MAX_BATTERY = 100
config.B_DRAIN_PER_DISTANCE = 1
config.SCOUT_ANT_COUNT = 20
config.MAIN_ANT_COUNT = 1000
config.EVAPORATION_RATE = 0.1


config.PRINT_STATS = True
config.PRINT_RATE = 100_000
config.DELAY_PRINT = 0
config.PRINT_BATTERY = True
config.PAUSE_ON_PRINT = False
config.PRINT_P_MEMORY = True
config.ADD_NODES_TYPE = 1
config.PRINT_P_STACK = False
config.PRINT_FINAL_POINTS = True
n=100
  
for i in range(n):
  test = EVRP.EVRP(points,charger, config)
  test.ACO()
  sleep(0.1)
  input()




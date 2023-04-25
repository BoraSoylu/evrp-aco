import EVRP
import numpy as np
from time import sleep
import os
import settings

points = np.random.randint(1, 101, size=(200 + 1, 2))
charger = np.random.randint(1, 101, size=(10, 2))
os.system('cls' if os.name == 'nt' else 'clear')

config:settings.config = settings.config

config.MAX_BATTERY = 200
config.B_DRAIN_PER_DISTANCE = 1

config.PRINT_STATS = True
config.PRINT_RATE = 1000
config.DELAY_PRINT = 0
config.PRINT_BATTERY = True
config.PAUSE_ON_PRINT = False
config.PRINT_P_MEMORY = True
config.ADD_NODES_TYPE = 2
config.PRINT_P_STACK = False
config.PRINT_FINAL_POINTS = True
n=10
  
for i in range(n):
  test = EVRP.EVRP(points,charger, config)
  test.testF()
  sleep(0.1)
  input()




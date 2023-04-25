import json
import collections
import numpy as np
class jsonSvc:
  def __init__(s):
      s.points = None
      s.chargers = None
      s.settings = None
      s.MAX_BATTERY = None
      s.MIN_ALLOWED_BATTERY = None
      s.RECHARGE_RATE = None
      s.B_DRAIN_PER_DISTANCE = None
      s.EVAPORATION_RATE = None
      s.SCOUT_ANT_COUNT = None
      s.MAIN_ANT_COUNT = None
      s.final_paths = []
      s.path_journeys = None
      s.pheromone_updates = []
      s.pheromone_single_update = []
      s.PHEROMONE_INTENSITY = 0
  def setScoutAndMainAntSize(s, scout, main):
      s.SCOUT_ANT_COUNT = scout
      s.MAIN_ANT_COUNT = main
  def setPointsAndChargers(s, points, chargers):
      s.points = points.tolist()
      s.chargers = chargers.tolist()
      
  def addToFinalPaths(s, path):
    s.final_paths.append(list(collections.deque(path)))
    
  def singlePheromoneUpdate(s, n1,n2,value):
    s.pheromone_single_update.append([int(n1),int(n2),float(value)])
  
  def addPheromoneIntensity(s,i):
    s.PHEROMONE_INTENSITY = i
  
  def addToPheromoneUpdate(s):
    if s.pheromone_single_update == []:
      return
    s.pheromone_updates.append(s.pheromone_single_update)
    s.pheromone_single_update = []
    
  def createJsonFile(s):
    for i in range(len(s.chargers)):
      s.chargers[i] = [int(s.chargers[i][0]),int(s.chargers[i][1])]
    for i in range(len(s.points)):
      s.points[i] = [int(s.points[i][0]),int(s.points[i][1])]
    for i in range(len(s.final_paths)):
      for j in range(len(s.final_paths[i])):
        s.final_paths[i][j] = int(s.final_paths[i][j])
    dictionary = {
      "SCOUT_ANT_COUNT" : s.SCOUT_ANT_COUNT,
      "MAIN_ANT_COUNT" : s.MAIN_ANT_COUNT,
      "points": s.points,
      "chargers": s.chargers,
      "final_paths": s.final_paths,
      "pheromone_updates": s.pheromone_updates,
      "PHEROMONE_INTENSITY": s.PHEROMONE_INTENSITY
    }
    json_object = json.dumps(dictionary, indent=4)
    with open('test.json', 'w') as f:
      json.dump(dictionary, f)
      
      
      
      
    # dictionary ={
    #   "points": [],
    #   "chargers": [],
    #   "settings": {
    #       "MAX_BATTERY": 100,
    #       "MIN_ALLOWED_BATTERY": 1,
    #       "RECHARGE_RATE": None,
    #       "B_DRAIN_PER_DISTANCE": 1,
    #       "EVAPORATION_RATE": 0,
    #       "SCOUT_ANT_COUNT": 100,
    #       "MAIN_ANT_COUNT": 100,
    #   },
    #   "final_paths": [],
    #   "path_journeys": [],
    #   "pheromone_updates": [],}

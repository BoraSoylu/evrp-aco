import numpy as np
import random
from collections import deque
from scipy.spatial import distance_matrix
from scipy.spatial.distance import cdist
from time import sleep
import math
import sys
import os
import settings
import jsonService
class EVRP:
  def __init__(s, points_coordinates:np.ndarray, chargers_coordinates:np.ndarray, config:settings.config):
    s.p = Stack() # Points stack
    s.v = Stack() # Visited points stack
    s.points_coordinates = points_coordinates
    s.start_point = s.points_coordinates[0]
    s.chargers_coordinates = chargers_coordinates
    s.distance_matrix = None
    s.pheromone_matrix = None
    s.MAX_BATTERY = config.MAX_BATTERY
    s.current_battery = s.MAX_BATTERY
    s.POINTS_NUM = s.points_coordinates.size // 2
    s.CHARGERS_NUM = s.chargers_coordinates.size // 2
    s.MOVE_DIVIDER = 'MOVE'
    s.MIN_ALLOWED_BATTERY = config.MIN_ALLOWED_BATTERY
    s.beginning = True
    s.RECHARGE_RATE = config.RECHARGE_RATE
    s.B_DRAIN_PER_DISTANCE = config.B_DRAIN_PER_DISTANCE
    s.EVAPORATION_RATE = config.EVAPORATION_RATE
    s.addNodesPickType = config.ADD_NODES_TYPE
    s.PHEROMONE_INTENSITY = config.PHEROMONE_INTENSITY
    s.step_count = 0
    s.p_stack_max_mem = 0
    s.config:settings.config = config
    s.jsonSvc = jsonService.jsonSvc()
    print('\n\n-----NEW----\n\n')
    s.createDistanceMatrix()
    s.createPheromoneMatrix()
    s.jsonSvc.setPointsAndChargers(points_coordinates, chargers_coordinates)
    s.v.push(0)
    s.jsonSvc.addPheromoneIntensity(s.PHEROMONE_INTENSITY)
    
  def testF(s):
    s.scout()
    return s.totalDistanceTravelled()
  
  def ACO(s):
    s.jsonSvc.setScoutAndMainAntSize(s.config.SCOUT_ANT_COUNT, s.config.MAIN_ANT_COUNT)
    for i in range(s.config.SCOUT_ANT_COUNT):
      s.addNodesPickType = 0
      s.scout()
      # if s.config.PRINT_STATS:
        # s.printStats(s.config.PRINT_RATE, s.config.DELAY_PRINT, 'run',True)
      print(f'Scout: {i}')
      s.updatePheromoneMatrixTest(False)
      s.resetValues()
      
    for i in range(s.config.MAIN_ANT_COUNT):
      s.clearConsole()
      s.addNodesPickType = 3
      s.scout()
      # if s.config.PRINT_STATS:
        # s.printStats(1, s.config.DELAY_PRINT, 'run',True)
      print(f'Main: {i}')
      s.updatePheromoneMatrixTest(False)
      s.resetValues()
      
        
    s.addNodesPickType = 2
    s.config.CLEAR_CONSOLE_ON_DONE=False
    s.scout()
    s.resetValues()
      
      
    s.jsonSvc.createJsonFile()
    return
  
  def clearConsole(s):
    os.system('cls' if os.name == 'nt' else 'clear')
    return

  def resetValues(s):
    s.current_battery = s.MAX_BATTERY
    s.v.resetContainer()
    s.p.resetContainer()
    s.v.push(0)
    s.step_count = 0
    s.beginning = True
    
  def printStats(s, mod, time, message, clear):
    if s.step_count % mod == 0:
      if clear:
        s.clearConsole()
      if message == 'run':
        print('\n-----------Running-----------\n')
      elif message == 'done' and s.addNodesPickType == 0:
        print('\n-----------Random Done-----------\n')
      elif message == 'done' and s.addNodesPickType == 1:
        print('\n-----------ACO Done-----------\n')
      elif message == 'done' and s.addNodesPickType == 3:
       print('\n-----------ACO Done-----------\n')
      elif message == 'done' and s.addNodesPickType == 2:
        print('\n-----------Greedy Done-----------\n')
      elif message == 'invalid':
        print('\n-----------Task Impossible-----------\n')
      elif message == 'greedy':
        print('\n-----------Greedy-----------\n')
        
      print(f'V stack: {s.v.container}')
      print(f'step_count is {s.step_count}')
      print(f'Distance travelled: {math.trunc(s.totalDistanceTravelled()):,}')
      if s.config.PRINT_BATTERY:
        print(f'Current battery: {int(s.current_battery)}')
      print(f'Chargers visited: {s.chargersVisited()}')
      if s.config.PRINT_P_MEMORY:
        print(f'P stack memory usage: {s.getStackMemSizeFormatted(s.p.container, True) }')
      if s.config.PRINT_P_STACK:
        print(f'P stack: {s.p.container}')
      if s.config.PAUSE_ON_PRINT:
        input()
      
      
      if message == 'done' and s.config.PRINT_FINAL_POINTS:
        print(f'\n --------- Points --------- \n{s.points_coordinates.tolist()}')
        print(f'\n --------- Chargers --------- \n{s.chargers_coordinates.tolist()}')
      elif message == 'invalid' and s.config.PRINT_FINAL_POINTS:
        print(f'\n --------- Points --------- \n{s.points_coordinates.tolist()}')
        print(f'\n --------- Chargers --------- \n{s.chargers_coordinates.tolist()}')
      
      
      # print(f'\n\n --------- P Stack --------- \n {s.p.container}')
      
      # print(f'\n\n P stack: {s.p.container}')
      sleep(time)

    
  
  def scout(s):
    while(True): 
      s.step_count = s.step_count + 1
      
      if s.config.PRINT_STATS:
        s.printStats(s.config.PRINT_RATE, s.config.DELAY_PRINT, 'run',True)
      
      # if last visited node is start node
      # and visited stacks size is not 1, end recursion 
      if s.v.top() == 0 and  s.v.size() > 1:
        s.printStats(1, s.config.DELAY_PRINT, 'done', s.config.CLEAR_CONSOLE_ON_DONE)
        s.jsonSvc.addToFinalPaths(s.v.container)
        s.jsonSvc.addToPheromoneUpdate()
        break
      
      # if beginning, populate point stack
      if s.beginning:
        s.beginning = False
        s.addNodes() # add nodes to p stack
        continue   
         
      # if we are out of possible moves, the task is impossible
      if not s.beginning and s.p.size() == 0:
        s.printStats(1, s.config.DELAY_PRINT, 'invalid', s.config.CLEAR_CONSOLE_ON_DONE)
        s.config.PRINT_STATS = False
        break
      
      # If we are out of moves, undo last move.
      if s.p.top() == s.MOVE_DIVIDER:
        s.p.pop() # Remove the move divider as we are undoing the last move
        
        # Notice that we are popping the v stack.
        s.undoDrainBattery(s.v.pop(), s.v.top()) # undo the battery drain
        continue      
      
      # if there is enough battery to move to the next drop-off point, move
      if s.enoughBatteryForMove(s.v.top(), s.p.top()):
        s.drainBattery(s.v.top(), s.p.top()) # simulate battery discharge
        s.v.push(s.p.pop()) # make move
        s.p.push(s.MOVE_DIVIDER) # add the move divider
        s.addNodes() # add new possible move nodes
        if s.v.top() < 0: # if we moved to a charger
          s.chargeBattery() # charge battery
        # s.printStats()
        continue
      
      # pop the last node of p as we don't have enough fuel to move to it
      s.p.pop()
    
  def chargersVisited(s):
    visitedChargers = 0
    for x in s.v.container:
      if x < 0:
        visitedChargers = visitedChargers + 1
    return visitedChargers
  
  def enoughBatteryForMove(s, p1,p2):
    if s.current_battery >= s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE:
      return True
    return False
  
  
  def addNodes(s):
    if s.addNodesPickType == 0:
      s.addNodesToStackRandom()  
    elif s.addNodesPickType == 1:
      s.addNodesToStackPheromoneGreedy() 
    elif s.addNodesPickType == 2:
      s.addNodesToStackGreedy()  
    elif s.addNodesPickType == 3:
      s.addNodesToStackPheromoneWeighted()  
    elif s.addNodesPickType == 666:
      s.addNodesToStackWorst()
    return
  
  # Add nodes randomly
  def addNodesToStackRandom(s):
    if s.v.top() >= 0: # !!! This forbids hopping between chargers.
      # Set seed and create a random array of chargers
      np.random.seed(None) 
      c_arr = np.random.permutation(np.arange(-1, -s.CHARGERS_NUM-1, -1))
      
      # Add the chargers to p first as we try to after trying all drop-off points
      for charger in c_arr:
        s.p.push(charger)
    
    # Set seed and create a random array of drop-off points
    np.random.seed(None)
    p_arr = np.random.permutation(np.arange(s.POINTS_NUM))
    
    no_nodes_left = True
    
    # Add drop-off to p if they are not in v
    for point in p_arr:
      if not s.v.exists(point):
        no_nodes_left = False
        s.p.push(point)
    if no_nodes_left:
      s.p.push(0) 
    
    return
  
  def addNodesToStackRandomGreedy(s, node_type):
    return
  
  def addNodesToStackPheromoneWeighted(s):
    points = np.arange(1,s.points_coordinates.size / 2,dtype=int)
    chargers = np.arange(-1,-s.chargers_coordinates.size / 2-1,-1,dtype=int)
    all_nodes = np.concatenate((points,chargers))
    
    not_visited = []
    for i in range(all_nodes.size):
      visited = False
      if all_nodes[i] > 0 and s.v.exists(all_nodes[i]):
        visited = True
      if not visited:
        not_visited.append(all_nodes[i]) 
    
    
    weights = []
    
    for i in range(len(not_visited)):
      weights.append(s.pheromone_matrix[s.v.top()][not_visited[i]])
    ###############################################################
    for i in range(len(weights)):
      weights[i] = 10 * weights[i]
    for i in range(len(weights)):
      weights[i] = 1 + weights[i]
      
    add_to_stack = []
    for i in range(len(not_visited)):
      chosen_node = random.choices(not_visited, weights=weights,k=1)[0]
      if not (s.v.top() < 0 and chosen_node<0):
        add_to_stack.append(chosen_node)
      index_of_node = not_visited.index(chosen_node)
      not_visited.pop(index_of_node)
      weights.pop(index_of_node)
      
    if len(add_to_stack) == 0:
      add_to_stack.append(0)

    all_visited = True
    
    for i in add_to_stack:
      if i > 0:
        all_visited = False
        
    if all_visited:
      s.v.push(0)
      return 
    
    s.addChargersFirst(add_to_stack)
    return

  def addInOrder(s,node_list):
    for i in reversed(node_list):
      s.p.push(i)
    return
  
  def addChargersFirst(s, node_list):
    for i in reversed(node_list):
      if i < 0:
        s.p.push(i)
      
    for i in reversed(node_list):
      if i >= 0:
        s.p.push(i)
    return

  
  def addNodesToStackPheromoneGreedy(s):
    if s.v.top() >= 0: # !!! This forbids hopping between chargers.
      arr = np.array([[-i, s.pheromone_matrix[s.v.top()][-i]] for i in range(1, s.CHARGERS_NUM)])
      # sortedArr = np.lexsort((arr[:, 0], arr[:, 1]))
      sortedArr = arr[arr[:, 1].argsort()]
      for element in sortedArr:
        s.p.push(int(element[0])) 
      
    nodes_not_visited = []
    
    for i in range(0, s.POINTS_NUM):
      if not s.v.exists(i):
        nodes_not_visited.append(i)
        
    if len(nodes_not_visited) == 0:
      s.v.push(0)
      return
    arr = np.array([[nodes_not_visited[i], s.pheromone_matrix[s.v.top()][nodes_not_visited[i]]] for i in range(0, len(nodes_not_visited))])
    
    sortedArr = arr[arr[:, 1].argsort()]
    
    for element in sortedArr:
      s.p.push(int(element[0])) 
    return
  
  def addNodesToStackGreedy(s): 
    if s.v.top() >= 0: # !!! This forbids hopping between chargers.
      arr = np.array([[-i, s.distance_matrix[s.v.top()][-i]] for i in range(1, s.CHARGERS_NUM)])
      # sortedArr = np.lexsort((arr[:, 0], arr[:, 1]))
      sortedArr = arr[arr[:, 1].argsort()]
      for element in reversed(sortedArr):
        s.p.push(int(element[0])) 
      
    nodes_not_visited = []
    
    for i in range(0, s.POINTS_NUM):
      if not s.v.exists(i):
        nodes_not_visited.append(i)
        
    if len(nodes_not_visited) == 0:
      s.v.push(0)
      return
    arr = np.array([[nodes_not_visited[i], s.distance_matrix[s.v.top()][nodes_not_visited[i]]] for i in range(0, len(nodes_not_visited))])
    
    sortedArr = arr[arr[:, 1].argsort()]
    
    for element in reversed(sortedArr):
      s.p.push(int(element[0])) 
       
    return
  
  def addNodesToStackWorst(s): # TODO: This is not done
    if s.v.top() >= 0: # !!! This forbids hopping between chargers.
      arr = np.array([[-i, s.distance_matrix[s.v.top()][-i]] for i in range(1, s.CHARGERS_NUM)])
      # sortedArr = np.lexsort((arr[:, 0], arr[:, 1]))
      sortedArr = arr[arr[:, 1].argsort()]
      for element in sortedArr:
        s.p.push(int(element[0])) 
      
    nodes_not_visited = []
    
    for i in range(0, s.POINTS_NUM):
      if not s.v.exists(i):
        nodes_not_visited.append(i)
        
    if len(nodes_not_visited) == 0:
      s.v.push(0)
      return
    arr = np.array([[nodes_not_visited[i], s.distance_matrix[s.v.top()][nodes_not_visited[i]]] for i in range(0, len(nodes_not_visited))])
    
    sortedArr = arr[arr[:, 1].argsort()]
    
    for element in sortedArr:
      s.p.push(int(element[0])) 
       
    return
  
  def addNodesToStackBruteForce(s, node_type):
    return
  
  
  def createPheromoneMatrix(s): # !!! Caveman code !!!
    # Combine the points_coordinates and chargers_coordinates arrays
    size = int(s.points_coordinates.size/2) + int(s.chargers_coordinates.size/2)
    s.pheromone_matrix = np.zeros((size,size))
    return
  # def createPheromoneMatrix(s): # !!! Caveman code !!!
  #   # Combine the points_coordinates and chargers_coordinates arrays
  #   all_nodes = np.concatenate((s.points_coordinates, np.flip(s.chargers_coordinates, axis=0)), axis=0)
  #   s.pheromone_matrix = distance_matrix(all_nodes, all_nodes, p=2)
  #   for i in range(len(all_nodes)):
  #     for j in range(len(all_nodes)):
  #       s.pheromone_matrix[i][j] = 0
  #   return
  
  def updatePheromoneMatrix(s,):
    
    return
  
  def updatePheromoneMatrixTest(s, evaporate):
    if evaporate:
      s.evaporate()
    new_stack = Stack()
    new_stack.container = s.v.container.copy()
    while not new_stack.is_empty():
      if new_stack.top() == 0 and new_stack.size() == 1:
        return
      a = new_stack.pop()
      b = new_stack.top()
      s.pheromone_matrix[a][b] = s.PHEROMONE_INTENSITY/s.totalDistanceTravelled() + s.pheromone_matrix[a][b]
      s.jsonSvc.singlePheromoneUpdate(a,b,s.pheromone_matrix[a][b])
    return
  def evaporate(s): # !!! Caveman Code !!!
    all_nodes = np.concatenate((s.points_coordinates, np.flip(s.chargers_coordinates, axis=0)), axis=0)
    for i in range(len(all_nodes)):
      for j in range(len(all_nodes)):
        s.pheromone_matrix[i][j] = s.pheromone_matrix[i][j] * s.EVAPORATION_RATE
    return
  
  def createDistanceMatrix(s):
    # Combine the points_coordinates and chargers_coordinates arrays
    all_nodes = np.concatenate((s.points_coordinates, np.flip(s.chargers_coordinates, axis=0)), axis=0)
    s.distance_matrix = distance_matrix(all_nodes, all_nodes, p=2)
    return
  
  def totalDistanceTravelled(s):
    newStack = Stack()
    newStack.container = s.v.container.copy()
    totalDistance = 0
    if newStack.size() == 1:
      return 0
    while(not newStack.is_empty()):
      totalDistance = totalDistance + s.distance_matrix[newStack.pop()][newStack.top()]
      if newStack.top() == 0:
        break
    return totalDistance
  
  def drainBattery(s, p1,p2):
    s.current_battery = s.current_battery - (s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE)
    return
  
  
  def undoDrainBattery(s, p1, p2):
    s.current_battery = s.current_battery + (s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE)
    return
  
  def chargeBattery(s):
    s.current_battery = s.MAX_BATTERY
    return
  
  def getStackMemSizeFormatted(s,d, bool):
    size = sys.getsizeof(d)
    for element in d:
        size += sys.getsizeof(element)
    if size < 1024:
        return f"{size}B"
    elif size < 1024**2:
        k, b = divmod(size, 1024)
        return f"{k}KB ({size}B)"
    else:
        m, k = divmod(size, 1024**2)
        return f"{m}MB ({size}B)"
      
  def formatMem(s,size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024**2:
        k, b = divmod(size, 1024)
        return f"{k}KB ({size}B)"
    else:
        m, k = divmod(size, 1024**2)
        return f"{m}MB ({size}B)"
      
  def getStackMemSize(s,d):
    size = sys.getsizeof(d)
    for element in d:
        size += sys.getsizeof(element)
    return size
  
     
    
  
class Stack:
  def __init__(s):
    s.container = deque()
  
  def push(s, val):
    s.container.append(val)
    
  def pop(s):
    return s.container.pop()
  
  def top(s):
    return s.container[-1]
  
  def is_empty(s):
    return False if s.container else True
  
  def size(s):
    return len(s.container) # this is O(1)? https://stackoverflow.com/questions/55516216/time-complexity-of-accessing-collections-deque-length
  
  def exists(s, val):
    return val in s.container
  
  def resetContainer(s):
    s.container = deque()
    return
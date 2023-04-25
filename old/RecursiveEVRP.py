import old.stack as stack
import numpy as np
from collections import deque
from scipy.spatial import distance_matrix
from time import sleep
class EVRP:
  def __init__(s, points_coordinates:np.ndarray, chargers_coordinates:np.ndarray):
    s.p = Stack() # Points stack
    s.v = Stack() # Visited points stack
    # s.c = Stack() # Chargers Stack
    s.points_coordinates = points_coordinates
    s.start_point = s.points_coordinates[0]
    s.chargers_coordinates = chargers_coordinates
    s.distance_matrix = None
    s.pheromone_matrix = None
    s.MAX_BATTERY = 100
    s.current_battery = s.MAX_BATTERY
    s.POINTS_NUM = s.points_coordinates.size // 2
    s.CHARGERS_NUM = s.chargers_coordinates.size // 2
    s.MOVE_DIVIDER = 'MOVE'
    s.MIN_ALLOWED_BATTERY = 1
    s.beginning = True
    s.RECHARGE_RATE = None
    s.B_DRAIN_PER_DISTANCE = 0.1
    s.EVAPORATION_RATE = None
    s.createDistanceMatrix()
    s.createPheromoneMatrix()
    s.AAAAAAAAA= 0
    s.v.push(0)
    
  def testF(s):
    s.scout()
    return
  
  def ACO(s):
    return
  
  def printStats(s):
    if not s.beginning:
      print()
      print('REEEEEEcursion')
    print(f'V is {s.v.container}')
    print(f'P is {s.p.container}')
    # sleep(0.05)
    
  
  def scout(s):
    s.AAAAAAAAA = s.AAAAAAAAA + 1

    

    # s.printStats()
    
    # if last visited node is start node
    # and visited stacks size is not 1, end recursion 
    if s.v.top() == 0 and  s.v.size() > 1:
      s.visitedNodes()
      return
    
    # if beginning, populate point stack
    if s.beginning:
      s.beginning = False
      s.addNodes() # add nodes to p stack
      s.scout()
      return
    
    # if we are out of possible moves, the task is impossible
    if s.v.top() == 0 and s.p.size() == 0:
      s.visitedNodes()
      return
    
    # If we are out of moves, undo last move.
    if s.p.top() == s.MOVE_DIVIDER:
      s.p.pop() # Remove the move divider as we are undoing the last move
      
      # # Since the last node that we've moved to is still in v stack
      # # it wont be added to p stack and we'll avoid making the
      # # same invalid move in the future.
      # s.addNodes() # Repopulate the points stack. 
      
      # Notice that we are popping the v stack.
      s.undoDrainBattery(s.v.pop(), s.v.top()) # undo the battery drain
      s.scout()
      return      
    
    # if there is enough battery to move to the next drop-off point, move
    if s.enoughBatteryForMove(s.v.top(), s.p.top()):
      s.drainBattery(s.v.top(), s.p.top()) # simulate battery discharge
      s.v.push(s.p.pop()) # make move
      s.p.push(s.MOVE_DIVIDER) # add the move divider
      s.addNodes() # add new possible move nodes
      if s.v.top() < 0: # if we moved to a charger
        s.chargeBattery() # charge battery
      s.scout() 
      return
    # else:
    #   print(f'no fuel for {s.p.top()}')
      
    
    # pop the last node of p as we don't have enough fuel to move to it
    s.p.pop()
    s.scout()
    return
    
  def visitedNodes(s):
    visitedChargers = 0
    for x in s.v.container:
      if x < 0:
        visitedChargers = visitedChargers + 1
    print(f'recursion count: {s.AAAAAAAAA}')
    print(f'visitedNodes {s.v.container}')
    print(f'Chargers visited: {visitedChargers}')
    return
  
  def enoughBatteryForMove(s, p1,p2):
    if s.current_battery >= s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE:
      return True
    return False
  
  # def makeMove(s, node_type):
  #   return
  
  def addNodes(s):
    s.addNodesToStackRandom()
    return
  
  def drainBattery(s, p1,p2):
    s.current_battery = s.current_battery - (s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE)
    # print(f'Drained to :{s.current_battery}')
    
    return
  
  def undoMove(s, node_type):
    return
  
  def undoDrainBattery(s, p1, p2):
    s.current_battery = s.current_battery + (s.distance_matrix[p1][p2] * s.B_DRAIN_PER_DISTANCE)
    return
  
  def chargeBattery(s):
    s.current_battery = s.MAX_BATTERY
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
  
  def addNodesToStackPheromone(s, node_type):
    return
  
  def addNodesToStackGreedy(s, node_type):
    return 
  
  def addNodesToStackBruteForce(s, node_type):
    return
  
  def createDistanceMatrix(s):
    # Combine the points_coordinates and chargers_coordinates arrays
    all_nodes = np.concatenate((s.points_coordinates, np.flip(s.chargers_coordinates, axis=0)), axis=0)
    s.distance_matrix = distance_matrix(all_nodes, all_nodes, p=2)
    return
  
  def createPheromoneMatrix(s):
    return
  
  def updatePheromoneMatrix(s):
    return
  
  def returnPath(s):
    return
  
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

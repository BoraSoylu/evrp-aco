class Stack:
  def __init__(self):
    self.container = deque()
  
  def push(self, val):
    self.container.append(val)
    
  def pop(self):
    return self.container.pop()
  
  def top(self):
    return self.container[-1]
  
  def is_empty(self):
    return False if self.container else True
  
  def size(self):
    return len(self.container)
  
  def exists(self, val):
    return val in self.container
  
  
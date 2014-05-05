"""Assignment 3, CS440/640, Spring 2014.  Logical Reasoning.

This module implements an logical agent and a world for it to explore.
"""
import logic
import logic_440

class WumpusWorldAgent(logic_440.KnowledgeBasedAgent):
  def __init__(self, cave_size):
    self.KB = logic.PropKB()
    self.size = cave_size
    for x in range(1, cave_size + 1):
      for y in range(1, cave_size + 1):
        pits = "("
        beast = "("
        neighbors = get_neighbors(x,y, cave_size)
        for z in range(len(neighbors)):
          pits = pits + ('P%d_%d'% neighbors[z])
          beast = beast + ('W%d_%d' % neighbors[z])
          if (z < len(neighbors) - 1):
            pits = pits + " | "
            beast = beast + " | "
        pits = pits + ")"
        beast = beast + ")"
        pit_rules = ('B%d_%d' % (x,y))
        beast_rules = ('S%d_%d' % (x,y))
        pit_rules = pit_rules + " <=> " + pits
        beast_rules = beast_rules + " <=> " + beast
        
        self.KB.tell(pit_rules)
        self.KB.tell(beast_rules)
      

  def safe(self):
    safe_zones = set()
    for x in range(1, self.size + 1):
      for y in range(1, self.size + 1):
        if(logic_440.resolution(self.KB, logic.Expr(('~W%d_%d' % (x,y)))) and logic_440.resolution(self.KB, logic.Expr(('~P%d_%d' % (x,y))))):
          safe_zones.add((x,y))

    return safe_zones
  
  def not_unsafe(self):
    not_unsafe_zones = set()
    for x in range(1, self.size + 1):
      for y in range(1, self.size + 1):
        if not (logic_440.resolution(self.KB, logic.Expr(('B%d_%d' % (x,y)))) | logic_440.resolution(self.KB,logic.Expr('S%d_%d' %(x,y)))):
          for z in get_neighbors(x,y,self.size):
            not_unsafe_zones.add(z)
        if not(logic_440.resolution(self.KB, logic.Expr(('P%d_%d' % (x,y)))) | logic_440.resolution(self.KB,logic.Expr('W%d_%d' %(x,y)))):
            not_unsafe_zones.add(z)                       
    return not_unsafe_zones
    
  def unvisited(self):
    unvisited = set()
    for x in range(1, self.size + 1):
      for y in range(1, self.size + 1):
        if not (logic_440.resolution(self.KB, logic.Expr(('L%d_%d' % (x,y))))):
          unvisited.add((x,y))
    return unvisited

NEIGHBOR_DELTAS = ((+1, 0), (-1, 0), (0, +1), (0, -1))

def get_neighbors(x, y, cave_size):
  possible_neighbors = [(x + dx, y + dy) for dx, dy in NEIGHBOR_DELTAS]
  return [(x1, y1) for x1, y1 in possible_neighbors if 
      1 <= x1 <= cave_size and 1 <= y1 <= cave_size]


class World:
  def __init__(self, size, gold, pits, wumpus):
    self.size = size
    self.gold = gold
    self.pits = pits
    self.wumpus = wumpus

  def perceive(self, (x, y), KB):
    print 'You enter room (%d, %d)' % (x, y)
    KB.tell('L%d_%d' % (x, y))

    if (x, y) in self.pits:
      print 'Oh no, you have fallen into a pit!'
      raise logic_440.GameOver(logic_440.RESULT_DEATH)
    else:
      KB.tell('~P%d_%d' % (x, y))

    if (x, y) == self.wumpus:
      print 'Oh no, you have wandered into the Wumpus\' room!'
      raise logic_440.GameOver(logic_440.RESULT_DEATH)
    else:
      KB.tell('~W%d_%d' % (x, y))

    if any((x1, y1) in self.pits for x1, y1 in get_neighbors(x,y, self.size)):
      print 'You feel a breeze'
      KB.tell('B%d_%d' % (x, y))
    else:
      KB.tell('~B%d_%d' % (x, y))

    if any((x1, y1) == self.wumpus for x1, y1 in get_neighbors(x,y, self.size)):
      print 'You smell a stench'
      KB.tell('S%d_%d' % (x, y))
    else:
      KB.tell('~S%d_%d' % (x, y))

    if (x, y) == self.gold:
      print 'You found the gold!'
      raise logic_440.GameOver(logic_440.RESULT_WIN)

def play(world):
  agent = WumpusWorldAgent(world.size)
  location = 1, 1
  try:
    while True:
      world.perceive(location, agent.KB)
      location = agent.choose_location()
  except logic_440.GameOver as e:
    print {logic_440.RESULT_WIN: 'You have won!',
           logic_440.RESULT_DEATH: 'You have died :(',
           logic_440.RESULT_GIVE_UP: 
           'You have left the cave without finding the gold :( '}[e.result]
    print
    print

def main():
  # Play a world with no Wumpus
  play(World(4, (2, 3), ((3, 1), (3, 3), (4, 4)), (-1, -1)))

  # Play a world with a Wumpus
  play(World(4, (2, 3), ((3, 1), (3, 3), (4, 4)), (1, 3)))

  # Feel free to make up additional worlds and see how your agent does at exploring them!

if __name__ == '__main__':
  main()

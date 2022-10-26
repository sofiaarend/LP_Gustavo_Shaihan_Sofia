from prettytable import PrettyTable

class FollowProds:
  def __init__(self, first, production):
    self.follow = first
    self.production = production


class Follow:
  def __init__(self, symbol):
    self.symbol = symbol
    self.follow_prod = []

  def append_follow(self, follow, production):
    self.follow_prod.append(FollowProds(follow, production))


class FollowTable:
  def __init__(self):
    self.follows = []
  
  def print_table(self):
    table = PrettyTable(['Símbolo', 'Follow'])
    for f in self.follows:
      follows = f.follow_prod[0].follow
      for p in f.follow_prod[1:]:
        follows += ', ' + p.follow
      table.add_row([f.symbol, follows])
    print(table)
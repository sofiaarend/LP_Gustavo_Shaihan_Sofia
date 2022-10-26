from prettytable import PrettyTable

class FirstProds:
  def __init__(self, first, production):
    self.first = first
    self.production = production


class First:
  def __init__(self, symbol):
    self.symbol = symbol
    self.first_prod = []

  def append_first(self, first, production):
    self.first_prod.append(FirstProds(first, production))

  def has_empty(self):
    for f in self.first_prod:
      if f.first == 'E':
        return True
    return False

  def remove_empty(self):
    has_empty = False
    for f in self.first_prod:
      if f.first == 'E':
        self.first_prod.remove(f)
        has_empty = True
    return has_empty


class FirstTable:
  def __init__(self):
    self.firsts = []

  def print_table(self):
    table = PrettyTable(['Símbolo', 'First'])
    for f in self.firsts:
      firsts = f.first_prod[0].first
      for p in f.first_prod[1:]:
        firsts += ', ' + p.first
      table.add_row([f.symbol, firsts])
    print(table)

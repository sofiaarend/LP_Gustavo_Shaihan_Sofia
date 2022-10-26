from symbol import term
from grammar_utils import *


def get_parsing_table(grammar, first_table, follow_table):
  types = get_types(grammar)
  terminals = types['terminals']
  terminals.append('$')

  parsing_table = [[0]]
  for cols in terminals:
    parsing_table[0] += [cols]

  non_terminals = types['non_terminals']
  for el in non_terminals:
    row = [el] + ['' for _ in range(len(terminals))]
    parsing_table.append(row)

  for f in first_table.firsts:
    symbol = f.symbol
    aux = next((x for x in parsing_table if x[0] == symbol), None)
    row = parsing_table.index(aux)

    for prod in f.first_prod:
      if prod.first == 'E':
        follows = next((x for x in follow_table.follows if x.symbol == symbol), None)
        for f_prod in follows.follow_prod:
          col = parsing_table[0].index(f_prod.follow)
          production = f_prod.production if f_prod.production else 'E'
          parsing_table[row][col] = symbol + '->' + production
      else:
        col = parsing_table[0].index(prod.first)
        parsing_table[row][col] = symbol + '->' + prod.production

  table = PrettyTable(parsing_table[0])    
  for row in parsing_table[1:]:
    table.add_row(row)
  print(table)
  return parsing_table


from symbol import term
from grammar_utils import *


def get_parsing_row(grammar, terminals, first):
  row = {}
  for char in terminals:
    # busca quais conjuntos first possuem aquele terminal
    firsts_contain = list(filter(lambda g: char in g['firsts'], first))
    for item in firsts_contain:
      # para cada conjunto encontra a regra na gramática
      prod_rule = list(filter(lambda g: g['left'] == item['symbol'], grammar))[0]
      for prods in prod_rule['productions']:
        # para cada regra busca qual producao possui o char
        if char in prods:
          row[char] = {'left': item['symbol'], 'right': prods}
  return row

def get_parsing_table(grammar):
  types = get_types(grammar)
  terminals = types['terminals']
  terminals.append('$')

  non_terminals = types['non_terminals']

  firsts = get_all_firsts(grammar)
  rows = get_parsing_row(grammar, terminals, firsts)

  parsing_table = [[0]]
  for el in non_terminals:
    row = [el] + ['' for x in range(len(terminals)+1)]
    parsing_table.append(row)

  for cols in terminals:
    parsing_table[0] += [cols]

  for key, obj in rows.items():
    col = parsing_table[0].index(key)
    row = -1
    for i in range(len(parsing_table)):
      if obj['left'] in parsing_table[i]:
        row = i

    parsing_table[row][col] = obj['left'] + '->' + obj['right']
  return parsing_table

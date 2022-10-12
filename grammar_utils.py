import re

# Ex:
# A -> Bb|c|d
# B -> f|E
# return [['A', ['Bb', 'c', 'd']], ['B', ['f', 'E']]]
def extract_pairs(str):
  grammar = []
  lines = str.replace(' ', '').split('\n')
  for line in lines:
    line = re.sub(r'/\s/', '', line)
    line = line.split('->')
    line[1] = line[1].split('|')
    grammar.append(line)
  return grammar

# return [{'left'=>'A', 'productions'=>['Bb', 'c', 'd']}, {'left'=>'B', 'productions'=>['f', 'E']}]
def pairs_to_object(grammar):
  final_grammar = []
  for prod_rule in grammar:
    final_grammar.append({
      'left': prod_rule[0],
      'productions': prod_rule[1]
    })
  return final_grammar

def is_non_terminal(symbol):
  return symbol != 'E' and re.search(r'^[A-Z]', symbol) != None

def is_terminal(symbol):
  return not is_non_terminal(symbol)

def get_types(grammar):
  terminals = []
  non_terminals = []
  for prod_rule in grammar:
    left = prod_rule['left']
    if is_non_terminal(left) and left not in non_terminals:
      non_terminals.append(left)
    elif is_terminal(left) and left not in terminals:
      terminals.append(left)

    for prods in prod_rule['productions']:
      for char in prods:
        if is_non_terminal(char) and char not in non_terminals:
          non_terminals.append(char)
        elif is_terminal(char) and char not in terminals:
          terminals.append(char)

  return {
    'terminals': terminals,
    'non_terminals': non_terminals
  }
      
def remove_duplicates(list):
  new_list = []
  for value in list:
    if value not in new_list:
      new_list.append(value)
  return new_list

# ----------------------
# --- First methods ---
# ----------------------
def get_symbol_firsts(grammar, productions, firsts):
  char = productions[0][0]
  if is_terminal(char):
    # se é terminal adiciona na lista
    firsts.append(char)
  else:
    # se não, busca os first do não terminal
    new_production = list(filter(lambda g: g['left'] == char, grammar))[0]['productions']
    firsts = get_symbol_firsts(grammar, new_production, firsts)
    if 'E' in firsts:
      # se os firsts do não terminal incluem a sentenca vazia, remove ela
      firsts.remove('E')
      if len(productions[0]) > 1 and is_terminal(productions[0][1]):
        # se após o não terminal tem um terminal, add ele por causa da sentenca vazia
        firsts.append(productions[0][1])

  if len(productions) > 1:
    return get_symbol_firsts(grammar, productions[1:], firsts)
  else:
    return firsts

def get_all_firsts(grammar):
  firsts_table = []
  for prod_rule in grammar:
    firsts = get_symbol_firsts(grammar, prod_rule['productions'], [])
    firsts_table.append({
      'symbol': prod_rule['left'],
      'firsts': remove_duplicates(firsts)
    })
  return firsts_table

# ----------------------
# --- Follow methods ---
# ----------------------
def get_symbol_positions(production, symbol):
  return [i for i, letter in enumerate(production) if letter == symbol]

def get_symbol_follow(grammar, symbol, history):
  if is_terminal(symbol):
    # se o símbolo for terminal retorna ele
    return [symbol]

  follow = []
  history = history.append(symbol) if history else []

  if symbol == grammar[0]['left']:
    # se o símbolo for o inicial da gramática add o símbolo de final de cadeia 
    follow.append('$')

  for prod_rule in grammar:
    for prods in prod_rule['productions']:
      # encontra todas as ocorrências do símbolo na producao
      positions = get_symbol_positions(prods, symbol)

      for i in positions:
        j = i
        while j < len(prods):
          if j+1 >= len(prods):
            # se for o último da producao
            new_symbol = prod_rule['left']
            if new_symbol not in history:
              # se o simbolo ainda não foi iterado, inclui o follow do lado esquerdo
              follow += get_symbol_follow(grammar, new_symbol, history)
            break
          else:
            next = prods[j+1]
            if is_non_terminal(next):
              # se o próximo símbolo não for terminal, busca seus first e add no follow
              next_prod = list(filter(lambda g: g['left'] == next, grammar))[0]['productions']
              firsts = get_symbol_firsts(grammar, next_prod, [])
              follow += remove_duplicates(firsts)

              if 'E' not in firsts:
                # somente testa o próximo simbolo se houver sentenca vazia no first
                break
            else:
              # se o próximo for terminal add no follow
              follow.append(next)
          j+=1
  return remove_duplicates(follow)

def get_all_follows(grammar):
  follow_table = []
  for prod_rule in grammar:
    first_symbol = prod_rule['left']
    follow = get_symbol_follow(grammar, first_symbol, [])
    follow_table.append({
      'symbol': prod_rule['left'],
      'follow': follow
    })
  return follow_table
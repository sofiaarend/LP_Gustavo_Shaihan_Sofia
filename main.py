import sys
from analysis_utils import *

from grammar_utils import *

def get_grammar():
  lines = []
  while True:
      line = input()
      if line == 'x':
        break
      else:
          lines.append(line)
  return '\n'.join(lines)

def main():
  print('!!! ANALISADOR PREDITIVO TABULAR !!!\n')
  print('Insira a gramática abaixo, uma regra por linha.\nPara finalizar insira "x" em uma nova linha.\n')
  
  grammar = pairs_to_object(extract_pairs(get_grammar()))

  print(f"\nGramática: {grammar}\n")
  firsts = get_all_firsts(grammar)
  print(f"Firsts: {firsts}\n")
  follow = get_all_follows(grammar)
  print(f"Follow: {follow}\n")

  parsing_table = get_parsing_table(grammar)
  print('--- TABELA DE ANALISE PREDITIVA ---\n')
  for line in parsing_table:
    print(f"{line}\n")


if (__name__ == "__main__"):
    main()
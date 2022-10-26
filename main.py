import sys
from analysis_utils import *
from follow import FollowTable

from grammar_utils import *
from sentence_utils import recognize_sentence

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

  first_table = FirstTable()
  get_all_firsts(grammar, first_table)
  first_table.print_table()
  
  follow_table = FollowTable()
  get_all_follows(grammar, follow_table)
  follow_table.print_table()

  print('\n--- TABELA DE ANALISE PREDITIVA ---\n')
  parsing_table = get_parsing_table(grammar, first_table, follow_table)

  while True:
    print('Insira a sentenca abaixo, seguido de enter. Insira x para encerrar o programa\n')
    sentence = input()
    if sentence =='x':
      sys.exit()

    response = recognize_sentence(sentence, grammar, parsing_table)
    print('--- TABELA DE ANALISE DA SENTENCA ---\n')
    if response['success']:
      print('Sentenca válida!!!\n')
    else: 
      print('Sentenca inválida :(\n')

    for row in response['table']:
      print(f"Pilha: {row['s']}; Entrada: {row['i']}; Saída: {row['o']}\n")


if (__name__ == "__main__"):
    main()
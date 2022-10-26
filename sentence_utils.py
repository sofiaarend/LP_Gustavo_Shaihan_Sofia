from grammar_utils import is_non_terminal


def recognize_sentence(input, grammar, parsing_table):
  sentence = list(input)
  sentence.append('$')

  stack = ['$', grammar[0]['left']]
  output = ''
  table = []

  aux_sentence = sentence.copy()
  table.append({ 's': ''.join(stack), 'i': ''.join(aux_sentence), 'o': output })

  while len(stack) > 0 and len(sentence) > 0:
    last = stack[-1]

    char = sentence[0]
    if last == char:
      sentence.remove(0)
      stack.pop(-1)
      output = ''
    else:
      if char not in parsing_table[0][1:]:
        break
      
      if is_non_terminal(last):
        col_char = parsing_table[0].index(char)
        print(col_char)
        aux = []
        for row in parsing_table:
          if last == row[0]:
            aux = row

        print(aux)
        prod = aux[col_char]
        print(prod)

        item = aux[col_char].split('->')[1]
        stack.pop(-1)
        stack.append(item[::-1])      
        output = last + '->' + aux
    
    if not len(stack) == 0 and not len(sentence) == 0:
      aux_sentence = sentence.copy()
      table.append({ 's': ''.join(stack), 'i': ''.join(aux_sentence), 'o': output })

  return {
    'success': len(stack) == 0 and len(input) == 0,
    'table': table
  }


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
    last = stack[-1][-1]
    char = sentence[0]

    if last == char:
      stack_aux = stack.copy()
      # Remove a prod antiga
      stack.pop(-1)
      if len(stack_aux[-1]) > 1:
          # Se a prod da stack sendo avaliada tiver mais de 1 char pega o resto dela
          stack_aux = ''.join(stack_aux[-1][:-1])
          # Add a prod sem o last na stack de novo
          stack.append(stack_aux)
      # Remove o char da sentenca
      sentence.pop(0)
      output = ''

    elif is_non_terminal(last):
      if char not in parsing_table[0][1:]:
        break
      
      # Se last for não terminal acha a coluna do terminal na tabela
      col_char = parsing_table[0].index(char)
      aux = []
      for row in parsing_table:
        # Acha a linha do last
        if last == row[0]:
          aux = row

      # Encontra a production do last e do char
      prod = aux[col_char]
      if len(prod) == 0:
        # Se não tiver production quebra pq é inválido
        break
      
      stack_aux = stack.copy()
      # Remove a prod antiga
      stack.pop(-1)
      if len(stack_aux[-1]) > 1:
        # Se a prod da stack sendo avaliada tiver mais de 1 char pega o resto dela
        stack_aux = stack_aux[-1][:-1]
        # Add a prod sem o last na stack de novo
        stack.append(stack_aux)

      # Add a nova prod na stack
      parts = prod.split('->')
      stack.append(parts[1][::-1])

      output = prod

    else:
      # Se os chars não forem iguais nem for não terminal
      # Quebra pq a sentenca é invalida e não tem para onde continuar
      break

    if len(stack) > 0 and len(sentence) > 0:
      aux_sentence = sentence.copy()
      table.append({ 's': ''.join(stack), 'i': ''.join(aux_sentence), 'o': output })

  return {
    'success': len(stack) == 0 and len(sentence) == 0,
    'table': table
  }


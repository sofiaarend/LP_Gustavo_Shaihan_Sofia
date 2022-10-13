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

    if last == sentence[0]:
      sentence.remove(0)
      stack.pop(-1)
      output = ''
    else:
      aux = []
      for row in parsing_table:
        if last == row[0]:
          aux = row

      if len(aux) == 0:
        break

      char_exists = 0
      for item in aux:
        if sentence[0] in item:
          char_exists = aux.index(item)
          break
      if char_exists == 0:
        break
      
      aux = aux[char_exists].split('->')[1]
      stack.pop(-1)
      stack.append(aux[::-1])

      output = last + '->' + aux
    
    if not len(stack) == 0 and not len(sentence) == 0:
      aux_sentence = sentence.copy()
      table.append({ 's': ''.join(stack), 'i': ''.join(aux_sentence), 'o': output })

  return {
    'success': len(stack) == 0 and len(input) == 0,
    'table': table
  }


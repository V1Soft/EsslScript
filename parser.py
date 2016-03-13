# parse function:
def parse(source):
    parsedScript = [[],[]]
    word = ''
    prevChar = ''
    inQuote = False
    inString = False
    inSingleComment = False
    inMultiComment = False

    # parse character by character:
    for char in source:

        # if CHAR is opening paranthesis:
        if char == '(' and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append WORD:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''

            # append list:
            parsedScript.append([])

        # if CHAR is closing paranthesis:
        elif char == ')' and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append WORD:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''

            # remove previous element:
            temp = parsedScript.pop()

            # append to previous list:
            parsedScript[-1].append(temp)

        # if CHAR is semicolon:
        elif char == ';' and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append WORD:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''

            # remove previous element:
            temp = parsedScript.pop()

            # append to previous list:
            parsedScript[-1].append(temp)

            # append list:
            parsedScript.append([])

        # if CHAR is sharp:
        elif char == '#' and not inQuote and not inString:

            # append '#':
            parsedScript[-1].append('#')

        # if CHAR is plus, minus, asterisk, forward slash, or caret:
        elif char in ('+', '-', '*', '/', '^') and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append WORD:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''
            parsedScript[-1].append(char)

        # if CHAR is space, tab, or newline:
        elif char in (' ', '\t', '\n') and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append WORD:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''

        # if CHAR is quote:
        elif char == '\'' and prevChar != '\\':

            # reverse INQUOTE value:
            inQuote = not inQuote

        # if CHAR is double quote:
        elif char == '\"' and prevChar != '\\':

            # reverse INSTRING value:
            inString = not inString

        # if else:
        else:

            # append CHAR to WORD:
            word += char

    # if CHAR is not space, tab, or newline:
    if char not in (' ', '\t', '\n') and not inQuote and not inString:

        # set PREVCHAR to CHAR
        prevChar = char

    # if WORD is not null:
    if word:

        # append WORD:
        parsedScript[-1].append(word)

        # set WORD to null:
        word = ''

    # return root list:
    return parsedScript[0]

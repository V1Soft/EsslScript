import sys
import readline

# variable class:
class Variable(object):
    def __init__(self, key):

        # variable name:
        self.key = key

        # variable value:
        self.value = None


# parse function:
def parse(source):
    parsedScript = [[],[]]
    word = ''
    prevChar = ''
    inQuote = False
    inString = False

    # parse character by character:
    for char in source:

        # if CHAR is opening paranthesis:
        if char == '(':

            # if WORD is not null:
            if word:

                # append word:
                parsedScript[-1].append(word)

                # set WORD to null:
                word = ''

            # append list:
            parsedScript.append([])

        # if CHAR is closing paranthesis:
        elif char == ')':

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
        elif char == ';':

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
        elif char == '#':

            # append '#':
            parsedScript[-1].append('#')

        # if CHAR is space, tab, or newline:
        elif char in (' ', '\t', '\n'):

            # if WORD is not null:
            if word:

                # append word:
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
    if char not in (' ', '\t', '\n'):

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

def execute(parsedScript='', preVars=[]):
    evaluatedScript = parsedScript
    variables = [Variable('stdin'), Variable('stdout'), Variable('stderr'), Variable('ret')]

    # append PREVAR elements to VARIABLES:
    for preVar in preVars:
        variables.append(preVar)

    # evaluate parsed codes from PARSE function:
    for code in evaluatedScript:
        try:
            # input:
            if code[0] == 'in':

                # set STDIN to INPUT
                for variable in variables:
                    if variable.key == 'stdin':
                        variable.value = input()

            # output VALUE,
            # output STREAM VALUE:
            elif code[0] == 'out':

                # if 3rd argument is not supplied:
                if len(code) == 2:

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # print variable value:
                                print(variable.value)
                                break

                    # if VALUE is not var:
                    else:

                        # print 2nd argument:
                        print(code[1])

                # if STREAM is var and 3rd argument is supplied:
                elif code[1][0] == '%' and len(code) == 3:

                    # if VALUE is var:
                    if code[2][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:
                                for variable2 in variables:
                                    if variable2.key == code[2][1:]:
                                        variable.value = variable2.value
                                        break
                                break

                        # if STREAM variable doesn't exist:
                        var = Variable(code[1][1:])
                        for variable in variables:
                            if variable.key == code[2][1:]:
                                var.value = variable.value

                        # append new var:
                        variables.append(var)

                    # if VALUE is INPUT:
                    elif code[2] == 'IN':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # set variable value to INPUT:
                                variable.value = input()
                                break

                        # if STREAM var doesn't exist:
                        var = Variable(code[1][1:])

                        # set variable value to INPUT:
                        var.value = input()
                        variables.append(var)

                    # if STREAM is not var:
                    else:
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # set variable value to 3rd argument:
                                variable.value = code[2]
                                break
                        var = Variable(code[1][1:])
                        var.value = code[2]
                        variables.append(var)

            # if EXPRESSION DO:
            elif code[0] == 'if':
                # if VALUE is VALUE2:
                if code[2] == '==':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value == variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var and VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value == code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] == code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE is not VALUE2:
                elif code[2] == '!=':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value != variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var and VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value != code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:
                        if code[1] != code[3]:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE is less than VALUE2:
                elif code[2] == '<':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value < variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var and VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value < code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] < code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE is greater than VALUE2:
                elif code[2] == '>':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value > variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value > code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] > code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE is less than or equal to VALUE2:
                elif code[2] == '<=':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value <= variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var and VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value <= code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] <= code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE greater than or equal to VALUE2:
                elif code[2] == '>=':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value >= variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var and VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value >= code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] >= code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

                # if VALUE is in VALUE2:
                elif code[2] == ':':

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:

                                # if VALUE and VALUE2 is var:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:

                                            # if EXPRESSION is true:
                                            if variable.value in variable2.value:

                                                # execute DO:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break

                                # if VALUE is var but VALUE2 is not var:
                                else:

                                    # if EXPRESSION is true:
                                    if variable.value in code[3]:

                                        # execute DO:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break

                    # if neither VALUE nor VALUE2 is var:
                    else:

                        # if EXPRESSION is true:
                        if code[1] in code[3]:

                            # execute DO:
                            execute(parsedScript=[code[4]], preVars=variables)

            # goto TAG:
            elif code[0] == 'goto':
                line = -1
                for tag in evaluatedScript:

                    # if code starts with sharp and tag value is 2nd argument:
                    if tag[0] == '#' and tag[1] == code[1]:

                        # execute script starting at line:
                        execute(evaluatedScript[line:], variables)

                    # increase line number by 1:
                    line += 1
                    #evaluatedScript.remove(code)

            # return VALUE:
            elif code[0] == 'ret':

                # if VALUE is var:
                if code[1][0] == '%':
                    for variable in variables:
                        if variable.key == 'ret':
                            for variable2 in variables:
                                if variable2.key == code[1][1:]:
                                    variable.value = variable2.value
                                    break
                            break
                else:
                    for variable in variables:
                        if variable.key == 'ret':
                            variable.value = code[1]
        except KeyboardInterrupt:
            exit(130)

args = []
i = 1

# parse arguments and pass to EXECUTE function:
for arg in sys.argv[2:]:
    variable = Variable(str(i))
    variable.value = arg
    args.append(variable)
    i += 1

# if argument count is greater than 1:
if len(sys.argv) > 1:

    # execute parsed 2nd argument:
    execute(parse(sys.argv[1]), args)

# if argument cound is 1 or less:
else:

    # print error:
    print('Invalid number of arguments.')

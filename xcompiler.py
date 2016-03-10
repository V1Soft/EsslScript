import sys
import readline

class Variable(object):
    def __init__(self, key):
        self.key = key
        self.value = None

def parse(source):
    parsedScript = [[],[]]
    word = ''
    prevChar = ''
    inQuote = False
    inString = False
    for char in source:
        if char == '(':
            if word:
                parsedScript[-1].append(word)
                word = ''
            parsedScript.append([])
        elif char == ')':
            if word:
                parsedScript[-1].append(word)
                word = ''
            temp = parsedScript.pop()
            parsedScript[-1].append(temp)
        elif char == ';':
            if word:
                parsedScript[-1].append(word)
                word = ''
            temp = parsedScript.pop()
            parsedScript[-1].append(temp)
            parsedScript.append([])
        elif char == '#':
            parsedScript[-1].append('#')
        elif char in (' ', '\t', '\n'):
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char == '\'' and prevChar != '\\':
            inQuote = not inQuote
        elif char == '\"' and prevChar != '\\':
            inString = not inString
        else:
            word += char
    if char not in (' ', '\t', '\n'):
        prevChar = char
    if word:
        parsedScript[-1].append(word)
        word = ''
    return parsedScript[0]

def execute(parsedScript='', preVars=[]):
    evaluatedScript = parsedScript
    variables = [Variable('stdin'), Variable('stdout'), Variable('stderr'), Variable('ret')]
    for preVar in preVars:
        variables.append(preVar)
    for code in evaluatedScript:
        try:
            # input:
            if code[0] == 'in':
                for variable in variables:
                    if variable.key == 'stdin':
                        variable.value = input()

            # output VALUE
            # output VALUE STREAM
            elif code[0] == 'out':
                if len(code) == 2:

                    # if VALUE is var:
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:
                                print(variable.value)
                                break
                    else:
                        print(code[1])

                # if VALUE is var:
                elif code[1][0] == '%' and len(code) == 3:

                    # if STREAM is var:
                    if code[2][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:
                                for variable2 in variables:
                                    if variable2.key == code[2][1:]:
                                        variable.value = variable2.value
                                        break
                                break
                        var = Variable(code[1][1:])
                        for variable in variables:
                            if variable.key == code[2][1:]:
                                var.value = variable.value
                        variables.append(var)

                    # set STREAM to input:
                    elif code[2] == 'IN':
                        for variable in variables:
                            if variable.key == code[1][1:]:
                                variable.value = input()
                                break
                        var = Variable(code[1][1:])
                        var.value = input()
                        variables.append(var)
                    else:
                        for variable in variables:
                            if variable.key == code[1][1:]:
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
                    if code[1][0] == '%':
                        for variable in variables:
                            if variable.key == code[1][1:]:
                                if code[3][0] == '%':
                                    for variable2 in variables:
                                        if variable2.key == code[3][1:]:
                                            if variable.value != variable2.value:
                                                execute(parsedScript=[code[4]], preVars=variables)
                                            break
                                    break
                                else:
                                    if variable.value != code[3]:
                                        execute(parsedScript=[code[4]], preVars=variables)
                                    break
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
                    if tag[0] == '#' and tag[1] == code[1]:
                        evaluate(evaluatedScript[line:], variables)
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

print(parse(sys.argv[1]))
args = []
i = 1
for arg in sys.argv[2:]:
    variable = Variable(str(i))
    variable.value = arg
    args.append(variable)
    i += 1
if len(sys.argv) > 1:
    execute(parse(sys.argv[1]), args)
else:
    print('Invalid number of arguments.')

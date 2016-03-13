import sys
import os
import inspect
import readline

import commands

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
        if char == '(' and not inQuote and not inString:

            # if WORD is not null:
            if word:

                # append word:
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

        # if CHAR is sharp, plus, minus, asterisk, forward slash, or modulus:
        elif char in ('#', '+', '-', '*', '/', '%') and not inQuote and not inString:

            # append '#':
            parsedScript[-1].append(char)

        # if CHAR is space, tab, or newline:
        elif char in (' ', '\t', '\n') and not inQuote and not inString:

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

def execute(parsedScript='', preVars=[]):
    script = parsedScript

    # append PREVAR elements to VARIABLES:
    for preVar in preVars:
        commands.variables.append(preVar)

    # evaluate parsed codes from PARSE function:
    for code in script:
        try:
            # input
            # input VALUE:
            if code[0] == 'in':
                if len(code) == 2:
                    commands.inCommand(code[1])
                elif len(code) == 1:
                    commands.inCommand()

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'in\'.')
                    sys.exit(1)

            # out VALUE
            # out VALUE VALUE2:
            elif code[0] == 'out':
                if len(code) == 2:
                    commands.outCommand(value=code[1])
                elif len(code) == 3:
                    commands.outCommand(code[1], code[2])

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'out\'.')
                    sys.exit(1)

            # if EXPRESSION DO:
            elif code[0] == 'if':
                if len(code) == 5:

                    # if EXPRESSION:
                    if ifCommand(code[1], code[2], code[3]):

                        # execute DO:
                        execute(parsedScript=[code[4]])

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'if\'.')
                    sys.exit(1)

            # goto TAG:
            elif code[0] == 'goto':
                if len(code) == 2:
                    execute(parsedScript=commands.gotoCommand(code[1]))

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'goto\'.')
                    sys.exit(1)

            # ret VALUE:
            elif code[0] == 'ret':
                if len(code) == 2:
                    commands.retCommand(code[1])

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'ret\'.')
                    sys.exit(1)
        except KeyboardInterrupt:
            exit(130)

args = []
i = 1

# parse arguments and pass to EXECUTE function:
for arg in sys.argv[3:]:
    variable = commands.Variable(str(i))
    variable.value = arg
    args.append(variable)
    i += 1

# if argument count is greater than 1:
if len(sys.argv) > 2:

    # if 2nd argument is 'run':
    if sys.argv[1] == 'run':

        # if ESSLFILE should be read from STDIN:
        if sys.argv[2][0] == '-':

            # parse and execute 3rd argument:
            execute(parse(sys.argv[2][1:]), args)

        # if ESSLFILE should not be read from STDIN:
        else:

            # set ESSLFILE to file given in 3rd argument:
            esslFile = open(sys.argv[2], 'r+')

            # parse and execute ESSLFILE:
            execute(parse(esslFile.read()), args)

    # if 2nd argument is not a recognized action:
    else:

        # print error:
        print('Action ' + sys.argv[1] + ' not found.')

# if argument cound is 1 or less:
else:

    # if 2nd argument is 'shell':
    if sys.argv[1] == 'shell':

        # set ret to 0:
        commands.getVar('stdret').value = 0
        while True:
            try:

                # set PWD to current directory:
                pwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

                # set COMMAND to INPUT:
                command = input('\n[' + str(commands.getVar('stdret').value) + '] '+ str(pwd) + ' : ')

                # set ESSLCOMMAND to parsed COMMAND:
                esslCommand = parse(command + ';')[0]

                # if INPUT is essl command:
                if esslCommand[0] in ('in', 'out', 'if', 'goto', 'ret'):

                    # parse and execute INPUT:
                    execute(parsedScript=[esslCommand])

                # if input is 'cd':
                elif esslCommand[0] == 'cd':
                    if len(esslCommand) == 2:

                        # change current directory:
                        os.chdir(esslCommand[1])

                        # return 0:
                        commands.getVar('stdret').value = 0

                    # print error:
                    else:
                        print('Incorrect number of arguments for command \'cd\'.')
                        commands.getVar('stdret').value = 1

                # if INPUT is 'help':
                elif esslCommand[0] == 'help':
                    print('\nin -- get user input and set to %stdin\nout <value> OR out <stream> <value> -- print to stdout or print to stream\nif <expression> <do> -- test expression and if true, execute following commands\ngoto <location> -- go to designated tag in script\nret <value> -- set return value\n')
                    # return 0:
                    commands.getVar('stdret').value = 0

                # if INPUT is 'exit':
                elif esslCommand[0] == 'exit':

                    # exit shell:
                    sys.exit(1)

                # if INPUT is not essl command:
                else:

                    # execute INPUT as system command:
                    os.system(command)
            except KeyboardInterrupt:

                # return Keyboard Interrupt code:
                commands.getVar('stdret').value = 130

    # if 2nd argument is not a recognized action:
    else:

        # print error:
        print('Invalid number of arguments.')

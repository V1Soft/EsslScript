import sys

import commands

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
                    return

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
                    return

            # if EXPRESSION DO:
            elif code[0] == 'if':
                if len(code) == 5:

                    # if VALUE is essl command:
                    if isinstance(code[1], list) and not isinstance(code[3], list):
                        execute([code[1]])

                        # if EXPRESSION is true:
                        commands.ifCommand(commands.getVar('ret').value, code[2], code[3])
                        if commands.getVar('ret').value == 'true':
                            execute(parsedScript=[code[4]])

                    # if VALUE is not essl command and VALUE2 is essl command:
                    elif not isinstance(code[1], list) and isinstance(code[3], list):
                        if not code[2] == ':':
                            execute([code[3]])

                        # if EXPRESSION is true:
                        commands.ifCommand(code[1], code[2], commands.getVar('ret').value)
                        if commands.getVar('ret').value == 'true':
                            execute(parsedScript=[code[4]])

                    # if VALUE and VALUE2 is essl command:
                    elif isinstance(code[1], list) and isinstance(code[3], list):
                        execute([code[1]])
                        valueRet = commands.getVar('ret').value
                        if not code[2] == ':':
                            execute([code[3]])
                            value2Ret = commands.getVar('ret').value
                        else:
                            value2Ret = code[3]

                        # if EXPRESSION is true:
                        commands.ifCommand(valueRet, code[2], value2Ret)
                        if commands.getVar('ret').value == 'true':
                            execute([code[4]])
                    else:
                        # if EXPRESSION is true:
                        commands.ifCommand(code[1], code[2], code[3])
                        if commands.getVar('ret').value == 'true':

                            # execute DO:
                            execute(parsedScript=[code[4]])

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'if\'.')
                    return

            # goto TAG:
            elif code[0] == 'goto':
                if len(code) == 2:
                    interpreter.execute(parsedScript=commands.gotoCommand(code[1]))

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'goto\'.')
                    return

            # expr VALUE OPERATOR VALUE2:
            elif code[0] == 'expr':
                if len(code) == 4:
                    commands.exprCommand(code[1], code[2], code[3])
                else:
                    print('Incorrect number of arguments specified for command \'expr\'.')
                    return

            # ret VALUE:
            elif code[0] == 'ret':
                if len(code) == 2:
                    commands.retCommand(code[1])

                # print error:
                else:
                    print('Incorrect number of arguments specified for command \'ret\'.')
                    return
        except KeyboardInterrupt:
            sys.exit(130)

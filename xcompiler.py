import sys
import os
import inspect
import readline

import commands
import parser
import interpreter

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
            interpreter.execute(parser.parse(sys.argv[2][1:]), args)

        # if ESSLFILE should not be read from STDIN:
        else:

            # set ESSLFILE to file given in 3rd argument:
            esslFile = open(sys.argv[2], 'r+')

            # parse and execute ESSLFILE:
            interpreter.execute(parser.parse(esslFile.read()), args)

    # if 2nd argument is not a recognized action:
    else:

        # print error:
        print('Action ' + sys.argv[1] + ' not found.')

# if argument cound is 1 or less:
else:

    # if 2nd argument is 'shell':
    if sys.argv[1] == 'shell':

        # set ret to 0:
        commands.getVar('ret').value = 0
        while True:
            try:

                # set PWD to current directory:
                pwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

                # set COMMAND to INPUT:
                command = input('\n[' + str(commands.getVar('ret').value) + '] '+ str(pwd) + ' : ')

                # set ESSLCOMMAND to parsed COMMAND:
                esslCommand = parser.parse(command + ';')[0]

                # if INPUT is essl command:
                if esslCommand[0] in ('in', 'out', 'if', 'goto', 'expr', 'ret'):

                    # parse and execute INPUT:
                    interpreter.execute(parsedScript=[esslCommand])

                # if input is 'cd':
                elif esslCommand[0] == 'cd':
                    if len(esslCommand) == 2:

                        # change current directory:
                        os.chdir(esslCommand[1])

                        # return 0:
                        commands.getVar('ret').value = 0

                    # print error:
                    else:
                        print('Incorrect number of arguments for command \'cd\'.')
                        commands.getVar('ret').value = 1

                # if INPUT is 'help':
                elif esslCommand[0] == 'help':
                    print('\nin -- get user input and set to %stdin\nout <value> OR out <stream> <value> -- print to stdout or print to stream\nif <expression> (do); -- test expression and if true, execute following commands\ngoto \'#\'<location> -- go to designated tag in script\nret <value> -- set return value\n')
                    # return 0:
                    commands.getVar('ret').value = 0

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
                commands.getVar('ret').value = 130

    # if 2nd argument is not a recognized action:
    else:

        # print error:
        print('Invalid number of arguments.')

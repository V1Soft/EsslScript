import sys
import readline

import interpreter

# variable class:
class Variable(object):
    def __init__(self, key):

        # variable type:
        self.objType = None # future strong, duck typing implementation

        # variable name:
        self.key = key

        # variable value:
        self.value = None

variables = [Variable('stdin'), Variable('stdin'), Variable('stderr'), Variable('ret')]

def getVar(var):
    keys = []
    for variable in variables:
        keys.append(variable.key)
    if var in keys:
        for variable in variables:
            if variable.key == var:
                return variable

    # if VAR does not exist:
    else:
        variables.append(Variable(var))
        return getVar(var)

def inCommand(stream=''):
    if stream:

        # if STREAM is essl command:
        if isinstance(stream, list):
            interpreter.execute([stream])
            getVar('ret').value = open(getVar('ret'), 'r+').read()

        # if STREAM is not essl command:
        else:

            # if STREAM is var:
            if stream[0] == '%':

                # set STDIN to value of STREAM given as file:
                getVar('ret').value = open(getVar(stream[1:]).value, 'r+').read()

            # if STREAM is not var:
            else:

                # set STDIN to INFILE:
                getVar('ret').value = open(value[1], 'r+').read()

    # if STREAM is not specified:
    else:

        # set STDIN to INPUT:
        getVar('ret').value = input()

# command class for 'out'
def outCommand(value='', value2=''):

    # if STREAM is not supplied:
    if value and not value2:

        # if VALUE is var:
        if value[0] == '%':

            # print variable value:
            print(getVar(value[1:]).value)

        # if VALUE is not var:
        else:

            # return VALUE:
            print(value)

    # if VALUE2 is specified:
    elif value and value2:

        # if VALUE2 is essl command:
        if isinstance(value2, list):

            # if VALUE is var:
            if value[0] == '%':
                interpreter.execute([value2])
                getVar(value[1:]).value = getVar('ret').value

            # print error:
            else:
                print('Error: Value must be variable.')
                sys.exit(1)

        # if VALUE2 is not essl command:
        else:

            #if VALUE is var:
            if value[0] == '%':

                # if VALUE and VALUE2 is var:
                if value2[0] == '%':
                    getVar(value[1:]).value = getVar(value2[1:]).value

                # if VALUE is var and VALUE2 is not var:
                else:

                    # set VALUE value to VALUE2:
                    getVar(value[1:]).value = value2

def ifCommand(value='', operator='', value2=''):
    # if VALUE is VALUE2:
    if operator == '==':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value == getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value == value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value == getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value == value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is not VALUE2:
    elif operator == '!=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value != getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value != value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value != getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value != value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is less than VALUE2:
    elif operator == '<':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value < getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value < value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value < getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value < value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is greater than VALUE2:
    elif operator == '>':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value > getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value > value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value > getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value > value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is less than or equal to VALUE2:
    elif operator == '<=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value <= getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value <= value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value <= getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value <= value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is greater than or equal to VALUE2:
    elif operator == '>=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value >= getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value >= value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value >= getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value >= value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    # if VALUE is in VALUE2:
    elif operator == ':':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value in getVar(value2).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value in value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value in getVar(value2[1:]).value:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value in value2:
                getVar('ret').value = 'true'
                return
            getVar('ret').value = 'false'

    else:
        print('Test Operator \'' + operator + '\' not found.')

def gotoCommand(script='', location=''):
    line = -1

    # if SCRIPT is essl command:
    if isinstance(location, list):
        interpreter.execute([location])
        for tag in script:

            # if TAG starts with sharp and TAG value is SCRIPT:
            if tag[0] == '#' and tag[1] == getVar('ret').value:

                # execute SCRIPT starting at LINE:
                return script[line:]

            # increase LINE by 1:
            line += 1
            #evaluatedScript.remove(code)

    # if SCRIPT is not essl command:
    else:
        for tag in script:

            # if TAG starts with sharp and TAG value is SCRIPT:
            if tag[0] == '#' and tag[1] == location:

                # execute SCRIPT starting at LINE:
                return script[line:]

            # increase LINE by 1:
            line += 1
            #evaluatedScript.remove(code)

def exprCommand(value='', operator='', value2=''):
    if operator == '+':
        getVar('ret').value = str(int(value) + int(value2))
    elif operator == '-':
        getVar('ret').value = str(int(value) - int(value2))
    elif operator == '*':
        getVar('ret').value = str(int(value) * int(value2))
    elif operator == '/':
        getVar('ret').value = str(int(value) / int(value2))
    elif operator == '^':
        getVar('ret').value = str(int(value) ** int(value2))
    else:
        print('Expression operator \'' + operator + '\' not found.')

def retCommand(value=''):
    try:

        # if VALUE is var:
        if value[0] == '%':
            getVar('ret').value = getVar(value[1:])

        # if VALUE is not var:
        else:
            getVar('ret').value = value

    # if return value is not int:
    except TypeError:
        print('Error: Return value type must be integer.')
        sys.exit(1)

import sys
import readline

# variable class:
class Variable(object):
    def __init__(self, key):

        # variable name:
        self.key = key

        # variable value:
        self.value = None

variables = [Variable('stdin'), Variable('stdin'), Variable('stderr'), Variable('stdret'), Variable('ret')]

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

        # if STREAM is var:
        if stream[0] == '%':

            # set STDIN to value of STREAM given as file:
            getVar('stdin').value = open(getVar(stream[1:]).value, 'r+').read()

        # if STREAM is not var:
        else:

            # set STDIN to INFILE:
            getVar('stdin').value = open(value[1], 'r+').read()

    # if STREAM is not specified:
    else:

        # set STDIN to INPUT:
        getVar('stdin').value = input()

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

    # if VALUE is var:
    elif value and value2:
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
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value == value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value == getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value == value2:
                return True

    # if VALUE is not VALUE2:
    elif operator == '!=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value != getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value != value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value != getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value != value2:
                return True

    # if VALUE is less than VALUE2:
    elif operator == '<':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value < getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value < value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value < getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value < value2:
                return True

    # if VALUE is greater than VALUE2:
    elif operator == '>':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value > getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value > value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value > getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value > value2:
                return True

    # if VALUE is less than or equal to VALUE2:
    elif operator == '<=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value <= getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value <= value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value <= getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value <= value2:
                return True

    # if VALUE is greater than or equal to VALUE2:
    elif operator == '>=':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value >= getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value >= value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value >= getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value >= value2:
                return True

    # if VALUE is in VALUE2:
    elif operator == ':':

        # if VALUE and VALUE2 is var:
        if value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value).value in getVar(value2).value:
                    return True

        # if VALUE is var and VALUE2 is not var:
        elif value[0] == '%' and not value2[0] == '%':

            # if EXPRESSION is true:
            if getVar(value[1:]).value in value2:
                return True

        # if VALUE is not var and VALUE2 is var:
        elif not value[0] == '%' and value2[0] == '%':

            # if EXPRESSION is true:
            if value in getVar(value2[1:]).value:
                return True

        # if neither VALUE nor VALUE2 is var:
        else:

            # if EXPRESSION is true:
            if value in value2:
                return True

    else:
        print('Test Operator \'' + operator + '\' not found.')

def gotoCommand(script=''):
    line = -1
    for tag in script:

        # if code starts with sharp and tag value is 2nd argument:
        if tag[0] == '#' and tag[1] == code[1]:

            # execute script starting at line:
            return script[line:]

        # increase line number by 1:
        line += 1
        #evaluatedScript.remove(code)

def exprCommand(value=''):
    getVar('ret').value = eval(value)

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

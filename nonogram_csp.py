'''
Construct and return nonogram CSP models.
'''

from cspbase import *

import itertools

def nonogram_csp_model_binary(initial_nonogram_cond_board):
    '''Return a CSP object representing a hitori CSP problem along  
       with an array of variables for the problem. That is return 

       hitori_csp, variable_array 

       where hitori_csp is a csp representing hitori using model_1 
       and variable_array is a list of lists 

       This routine returns Model_1 which consists of a variable for 
       each cell of the board, with domain equal to {0,i}, with i being 
       the initial value of the cell in the board.  

       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between 
       all relevant variables (e.g., all pairs of variables in the 
       same row, etc.) 

       All of the constraints of Model_1 MUST BE binary constraints  
       (i.e., constraints whose scope includes exactly two variables). 
    '''

    ##IMPLEMENT
    n = len(initial_nonogram_cond_board['hor'])
    m = len(initial_nonogram_cond_board['ver'])

    varMap = [None] * m
    varRowMap = [None] * (n * m)

    # todo: have to modify domain [0] -> if empty.
    for i in range(0, m):
        varMap[i] = [None] * n
        for j in range(0, n):
            varMap[i][j] = Variable('N{},{}'.format(i, j), [0, 1])
            varRowMap[i * n + j] = varMap[i][j]

    cons = []
    # make constraint from rows
    for i in range(m):
        cons_str = "C("
        cons_list = [None] * n
        domain_list = list()
        for j in range(n):
            # make string for constraint
            cons_str += ('N' + str(i) + ','+ str(j))
            if j < n - 1:
                cons_str += ','
                # make a list for constraint
            cons_list[j] = varMap[i][j]
            domain_list.append([0,1])
        cons_str += ')'


        con = Constraint(cons_str, cons_list)
        sat_tuples = []

        cond = initial_nonogram_cond_board['ver'][i]
        if len(cond) != 0:
            for t in itertools.product(*domain_list):
                if valid_for_binary(t, cond):
                    sat_tuples.append(t)
        else:   #[0,0,0,0,0,....,0]
            t = [0] * n
            sat_tuples.append(t)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)


    # make constraint from columns
    for i in range(n):
        cons_str = "C("
        cons_list = [None] * m
        domain_list = list()
        for j in range(m):
            # make string for constraint
            cons_str += ('N' + str(j) + str(i))
            if j < m - 1:
                cons_str += ','
                # make a list for constraint
            cons_list[j] = varMap[j][i]
            domain_list.append([0, 1])
        cons_str += ')'

        con = Constraint(cons_str, cons_list)
        sat_tuples = []
        cond = initial_nonogram_cond_board['hor'][i]

        if len(cond) != 0 :
            for t in itertools.product(*domain_list):
                if valid_for_binary(t, cond):
                    sat_tuples.append(t)
        else:   #[0,0,0,0,0,....,0]
            t = [0] * m
            sat_tuples.append(t)

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    nonogram_csp = CSP("{} by {}-Nonogram".format(m, n), varRowMap)

    for c in cons:
        nonogram_csp.add_constraint(c)

    return nonogram_csp, varMap


##############################


#Color

def valid_for_binary(checkList, condition):
    n = len(checkList)
    cm = len(condition)

    cur = 0
    cur_cond = condition[cur]
    increasing = 0
    restPoint = False
    finished = False

    #should consider condition list do not have any conditions.
    for i in range(0, n):
        if checkList[i] is 0:
            if restPoint is True:
                restPoint = False
                cur_cond = condition[cur]
            if increasing is not 0:
                return False
        else :
            if finished is True or restPoint is True:
                return False

            increasing += 1
            if cur_cond is increasing:
                cur += 1
                increasing = 0
                restPoint = True
                if cur >= cm:
                    finished = True
                    restPoint = False


    if finished :
        return True
    else :return False
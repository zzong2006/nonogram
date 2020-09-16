from cspbase import *
from orderings import *
from propagators import *
from nonogram_csp import *


import itertools

# 1. making constraints

# nonogram = {"ver":[[1,2],[1,3],[1,1,1],[2],[1,1],[4],[2,1],[2,1],[3],[1]],
# "hor":[[3,2],[5],[4,1,1],[2,1,2,2],[2,2,1]]}
# sample,variables = nonogram_csp_model_binary(nonogram)
#
# btracker = BT(sample)
#btracker.trace_on()
# You can turn on the backtracking tracing or not.

# print("Forward Checking on simple CSP, with MRV & LCV")
# btracker.bt_search(prop_FC, ord_mrv, val_lcv)
# print("=======================================================")
# print("GAC on simple CSP, with MRV & LCV")
# btracker.bt_search(prop_GAC, ord_dh, val_lcv)


# 2 . Now n-Queens example

def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj 
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i - j) != abs(qi - qj)


def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i + 1)
    # dom = 1,2,3,4,5,6.... n

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))
    # vars : [Var-Q1, Var-Q2, Var-Q3, Var-Q4, Var-Q5, Var-Q6, Var-Q7, Var-Q8]

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi + 1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi + 1, qj + 1), [vars[qi], vars[qj]])
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp


def solve_nQueens(n, propType, var_ord_type, val_ord_type, trace=False):
    csp = nQueens(n)
    solver = BT(csp)
    if trace:
        solver.trace_on()
    if propType == 'BT':
        solver.bt_search(prop_BT, var_ord_type, val_ord_type)
    elif propType == 'FC':
        solver.bt_search(prop_FC, var_ord_type, val_ord_type)
    elif propType == 'GAC':
        solver.bt_search(prop_GAC, var_ord_type, val_ord_type)


# trace = True
trace = False
print("Plain Bactracking on 8-queens w/MRV & LCV")
solve_nQueens(8, 'FC', ord_mrv, val_lcv, trace)
# print("=======================================================")
# print("Plain Bactracking on 8-queens w/DH & LCV")
solve_nQueens(8, 'FC', ord_dh, val_lcv, trace)
print("=======================================================")


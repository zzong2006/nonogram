#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import operator
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.
     var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp, var = None):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''
#IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    minIndex = 0
    i = 0
    min = -1

    for var in vars:
        if var.assignedValue == None:
            count = len(var.cur_domain())
            if min < 0 or min > count:
                min = count
                minIndex = i
        i += 1

    return vars[minIndex]


def ord_dh(csp, var = None):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node,
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''
#IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    maxVar = None

    max = -1
    for var in vars:
        count = 0
        if var.assignedValue == None:
            for scopeVar in csp.get_cons_with_var(var):
                for othervar in scopeVar.scope:
                    if othervar.name != var.name and othervar.assignedValue == None:
                        count += 1

            if max < 0 or max < count:
                max = count
                maxVar = var

    return maxVar



def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain
    values in other variables that share at least one constraint with var.
    '''
#IMPLEMENT
    #more available domain is highest value.
    result = list()
    temp = var.cur_domain()
    val = len(csp.get_all_vars())
    vars = csp.get_all_vars()
    varCons = csp.get_cons_with_var(var);
    rosting = {}
    assigned = set()

    for vart in temp :
        countlist = list()

        for i in range(val):
            countlist.append(set())

        for const in varCons:
            mainIndex = const.scope.index(var)
            if (var, vart) not in const.sup_tuples:
                continue

            #domain <-> scope (i.e. Var-Z = 0 in scope but vars in 2)
            matching = [None] * len(const.scope)
            for i, const_vart in enumerate(const.scope):
                insert = vars.index(const_vart)
                matching[i] = insert
                #already assigned give full domain
                if(const_vart.assignedValue != None):
                    assigned.add(insert)

            t = const.sup_tuples[(var, vart)]
            for tup in t:
                for j, tupNum in enumerate(tup):
                    if j != mainIndex:
                       countlist[matching[j]].add(tupNum)
        count = 0

        for i in range (0,len(countlist)):
            if i in assigned:
                count += len(vars[i].dom)
            else:
                count += len(countlist[i])

        rosting[vart] = count

    #make a list for each value
    #ex. {1: 42, 2: 40, 3: 38, 4: 38, 5: 38, 6: 38, 7: 40, 8: 42}
    #ex. [1, 8, 2, 7, 3, 4, 5, 6]

    sorted_x = sorted(rosting.items(), key=operator.itemgetter(1), reverse=True)

    for i in sorted_x:
        result.append(i[0])

    return result

def ord_inOrder(csp, var = None):
    for x in csp.get_all_unasgn_vars():
        return x

def ord_custom(csp, map):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''
    vars = csp.get_all_vars()

    added_val_row = [0] * len(map['hor'])
    added_val_col = [0] * len(map['ver'])

    for i in range(len(map['ver'])):
        for x in map['ver'][i]:
            added_val_col[i] += x

    for i in range(len(map['hor'])):
        for x in map['hor'][i]:
            added_val_row[i] += x

    for i in range(len(map['ver'])):
        for j in range(len(map['hor'])):
            if vars[i * len(map['hor']) + j] is not None:
                added_val_col[i] -= 1
                added_val_row[j] -= 1

    maxvar = 0
    max = -1
    count = 0

    for i in range(len(map['ver'])):
        for j in range(len(map['hor'])):
            count += added_val_col[i]
            count += added_val_row[j]

            if (max == -1 or max < count) and (vars[i * len(map['hor']) + j].assignedValue is None):
                max = count
                maxvar = vars[i * len(map['hor']) + j]

            count = 0

    return maxvar
#IMPLEMENT
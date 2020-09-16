from queue import *
import itertools
'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

Consider implementing propagators for forward checking or GAC as a course project!

'''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        # check whether there is no assigned variables.
        if c.get_n_unasgn() == 0:
            # all assigned Variables -> check possible or deadend.
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


# False: deadend detected.
# What variable want to be returned?
'''
The list of variable values pairs are all of the values
the propagator pruned (using the variable's prune_value method).
bt_search NEEDS to know this in order to correctly restore these
values when it undoes a variable assignment.
'''


# have to find out the check possible whether I selected other one.

def prop_FC(csp, newVar=None):
    pruned_list = []

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        remain = c.get_n_unasgn()
        vals = []
        vars = c.get_scope()
        if remain == 0:
            # all assigned Variables -> check possible or deadend.
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                print('line is wrong!')
                return False, []
        # we still have variables to assign.
        else:
            # make a list until last initiated variable.

            for i, var in enumerate(vars):
                vals.append((i, var.get_assigned_value()))
            # vals = [(0,None),(1,1),(2,None)....]

            # list unassigned variables.
            unMarried = c.get_unasgn_vars()
            for var in unMarried:
                index = vars.index(var)

                for x in var.cur_domain():
                    temp = vals[:]
                    nope = True
                    temp[index] = (index, x)

                    sup_tup = c.sup_tuples.get((var, x))

                    if sup_tup is not None:
                        for sup_c in sup_tup:
                            # you must find out the way to compare.
                            if checkIncludeTuple(temp, sup_c):
                                # this assigned is find.
                                nope = False
                                break
                        if nope is True:
                            var.prune_value(x)
                            pruned_list.append((var, x))
                            if var.cur_domain_size() is 0:
                                return False, pruned_list
                                # delete this domain from the cur variable
                    else:
                        var.prune_value(x)
                        pruned_list.append((var,x))
                        if var.cur_domain_size() is 0:
                            return False, pruned_list

    return True, pruned_list


def prop_GAC(csp, newVar=None):
    GACQueue = Queue()
    pruned_list = list()

    if not newVar:
        for c in csp.get_all_cons():
            scp = c.get_scope()
            for var in scp :
                GACQueue.put((c,var))

        while GACQueue.empty() is not True:
            cons, var = GACQueue.get() #TDA ←TDA  \ {⟨X,c⟩};
            #index = cons.index(var)
            for x in var.cur_domain():
                domain_list = []
                checkingError = False

                for sc_var in cons.get_scope():
                    if sc_var is var:
                        domain_list.append([x])
                    else:
                        domain_list.append(sc_var.cur_domain())

                for t in itertools.product(*domain_list):
                    if cons.check(t) is True:
                        checkingError = True
                        break

                #this should be modified
                if checkingError is False:
                    var.prune_value(x)
                    pruned_list.append((var, x))

                    #delete cons from the list.
                    # TDA ←TDA ∪{⟨Z,c'⟩|X ∈scope(c'), c' is not c, Z∈scope(c') \ {X} }

                    adding_list = csp.get_cons_with_var(var)
                    adding_list.remove(cons)

                    for add_con in adding_list:
                        adding_vars = add_con.get_scope()
                        adding_vars.remove(var)

                        for add_var in adding_vars:
                            GACQueue.put((add_con, add_var))
                    #DWO
                    if var.cur_domain_size() is 0:
                        return False, pruned_list

                #D_x ←ND_x
        return True, pruned_list
    else:
        for c in csp.get_all_cons():
            scp = c.get_scope()
            for var in scp :
                if var.is_assigned() is False:
                    GACQueue.put((c,var))

        while GACQueue.empty() is not True:
            cons, var = GACQueue.get() #TDA ←TDA  \ {⟨X,c⟩};
            #index = cons.index(var)
            for x in var.cur_domain():
                domain_list = []
                checkingError = False

                for sc_var in cons.get_scope():
                    if sc_var is var:
                        domain_list.append([x])
                    elif sc_var.is_assigned() is True:
                        domain_list.append([sc_var.get_assigned_value()])
                    else:
                        domain_list.append(sc_var.cur_domain())

                for t in itertools.product(*domain_list):
                    if cons.check(t) is True:
                        checkingError = True
                        break

                #this should be modified
                if checkingError is False:
                    var.prune_value(x)
                    pruned_list.append((var, x))

                    #delete cons from the list.
                    # TDA ←TDA ∪{⟨Z,c'⟩|X ∈scope(c'), c' is not c, Z∈scope(c') \ {X} }

                    adding_list = csp.get_cons_with_var(var)
                    adding_list.remove(cons)

                    for add_con in adding_list:
                        adding_vars = add_con.get_scope()
                        adding_vars.remove(var)

                        for add_var in adding_vars:
                            GACQueue.put((add_con, add_var))
                    #DWO
                    if var.cur_domain_size() is 0:
                        return False, pruned_list

                            #D_x ←ND_x
        return True, pruned_list



def checkIncludeTuple(small, big):
    for i, tup in enumerate(small):
        if tup[1] is None:
            continue
        else:
            if tup[1] != big[i]:
                return False

    return True




from tkinter import *
from orderings import *
from propagators import *
from nonogram_csp import *
from tkinter.scrolledtext import ScrolledText

import ast

var =''
def find_max(data):
    maxi = 0
    for i in range(len(data)):
        if len(data[i]) > maxi:
            maxi = len(data[i])
    return maxi

class Block:
    def __init__(self, color='white'):
        self.color = color

class Constraint:
    def __init__(self, const_num):
        self.const_num = const_num

def nonogrid_maker(root, row_col_dict, grid_dict):
    ver = row_col_dict["hor"]
    hor = row_col_dict["ver"]

    hor_con_size = find_max(hor)
    ver_con_size = find_max(ver)

    for i in range(len(hor)):
        i_size = len(hor[i])
        for con in range(len(hor[i])):
            temp = Constraint(hor[i][con])
            grid_dict[(ver_con_size + i, hor_con_size - i_size)] = [temp]
            i_size = i_size - 1
            
    for i in range(len(ver)):
        i_size = len(ver[i])
        for con in range(len(ver[i])):
            temp = Constraint(ver[i][con])
            grid_dict[(ver_con_size - i_size, hor_con_size + i)] = [temp]
            i_size = i_size - 1

    for r in range(ver_con_size + len(hor)):
        for c in range(hor_con_size + len(ver)):
            if ((r > ver_con_size -1) and (c < hor_con_size)) or ((r < ver_con_size) and (c > hor_con_size - 1)):
                if (r,c) in grid_dict:
                    w = Button(root, text = grid_dict[(r,c)][0].const_num, height = 1, width = 1)
                    w.grid(row=r, column=c)
                    grid_dict[(r,c)].append(w)
                else:
                    temp = Constraint('')
                    grid_dict[(r,c)] = [temp]
                    w = Button(root, text = grid_dict[(r,c)][0].const_num, height = 1, width = 1)
                    w.grid(row=r, column=c)
                    grid_dict[(r,c)].append(w)
            elif (r > ver_con_size - 1) and (c > hor_con_size - 1):
                grid_dict[(r,c)] = [Block()]
                w = Label(root, text='', bg='white', height = 1, width = 1)
                w.grid(row=r, column=c)
                grid_dict[(r,c)].append(w)
    return root

def change_input(row, col, grid_dict):
    # toplevel = Toplevel()
    # entry = Entry(toplevel)
    # entry.pack()
    # entry.focus_set()
    # b = Button(toplevel, text="OKAY", command = change_it(row, col, grid_dict, entry.get()))
    return 0

def change_it(row, col, grid_dict, val):
    grid_dict[(row, col)][0].const_num = val


class Nonogram():
    def __init__(self, row_col_dict):
        self.root = Tk()
        self.grid_dict = {}
        self.hor_con_size = find_max(row_col_dict["ver"])
        self.ver_con_size = find_max(row_col_dict["hor"])
        self.nono_grid = nonogrid_maker(self.root, row_col_dict, self.grid_dict)
        self.ver, self.hor = self.root.grid_size()
        self.row_col_dict = row_col_dict

        self.panel_maker_1()

        self.cmd = ''

        self.note = ScrolledText(self.root, height=10, width=52)
        result = "%3s%8s%15s%14s\n" % ("Mode", " # SolvingTime /", " Assigned_VAR /", "# Pruned_VAR")

        self.note.insert(INSERT, result)
        self.note.insert(END, '----------------------------------------------------\n')
        self.note.configure(state=DISABLED)

        #root -> grid
        self.note.grid(row=4, column=self.ver+1, rowspan=10, columnspan=52)

        self.is_tracing_On = IntVar()
        self.tracing_cb = Checkbutton(self.root, text="Tracing Mode", variable = self.is_tracing_On)
        self.tracing_cb.grid(row = 10, column = int(self.ver) )

        self.solve_button = Button(self.root, text="SOLVE", bg="black", foreground="white", command = self.solve_it)
        self.solve_button.grid(row = 11, column = self.ver)
        self.save_button = Button(self.root, text="SAVE", bg="white", foreground = "red", command = self.out_it)
        self.save_button.grid(row = 14, column = self.ver)
        self.load_button = Button(self.root, text="LOAD", bg="white", foreground = "red", command = self.load_it)
        self.load_button.grid(row = 15, column = self.ver)
        self.quit_button = Button(self.root, text="Quit", bg="green", foreground="white", command=self.root.destroy)
        self.quit_button.grid(row = 18, column = self.ver)

    def set(self, row, column, value):
        widget = self.grid[row][column]
        widget.configure(text=value)

    def solve_it(self):
        #PLACE RUNNING CODE HERE 
        #AND USE self.cmd as in   whatever(self.cmd)
        #also make self.save_button

        nono_csp, variables = nonogram_csp_model_binary(self.row_col_dict)

        btracker = BT(nono_csp)
        btracker.board = self.row_col_dict

        solve_method = self.cmd

        VarAssign = 0
        VarPruned = 0

        # make board white
        self.color_out()

        if solve_method is 1:
            if  self.is_tracing_On.get() == 1:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_FC, ord_mrv, val_lcv, self)
            else:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_FC, ord_mrv, val_lcv)
        elif solve_method == 2:
            if self.is_tracing_On.get() == 1:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_GAC, ord_dh, val_lcv, self)
            else:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_GAC, ord_dh, val_lcv)
        elif solve_method == 3 :
            if self.is_tracing_On.get() == 1:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_GAC, ord_inOrder, val_lcv, self)
            else:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_GAC, ord_inOrder, val_lcv)
        elif solve_method == 4:
            if self.is_tracing_On.get() == 1:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_FC, ord_custom, val_lcv, self)
            else:
               result, solving_time, VarAssign, VarPruned = btracker.bt_search(prop_FC, ord_custom, val_lcv)
        else :
            result = []
            solving_time = -1
        if len(result) > 0 :
            colour_in(self.root, result, self.grid_dict, self.ver, self.hor)

        text_in(self, solve_method, solving_time, VarAssign, VarPruned)

    def out_it(self):
        self.master = Tk()
        self.e2 = ScrolledText(self.master, width = 40, height = 30)
        self.e2.insert(INSERT, str(self.row_col_dict))
        self.e2.pack()
        self.e2.configure(state=DISABLED)

    def panel_maker_1(self):
        self.var1 = IntVar()
        R1 = Radiobutton(self.root, text="FC + MRV", variable=self.var1, value=1, command=self.sel1)
        R1.grid(row = 6, column = self.ver, sticky=W)

        R2 = Radiobutton(self.root, text="FC + DH", variable=self.var1, value=2, command=self.sel1)
        R2.grid(row = 7, column = self.ver, sticky=W)

        R1 = Radiobutton(self.root, text="FC + CUSTOM", variable=self.var1, value=4, command=self.sel1)
        R1.grid(row=  8, column=self.ver, sticky=W)

        R3 = Radiobutton(self.root, text="GAC", variable=self.var1, value=3, command=self.sel1)
        R3.grid(row = 9, column = self.ver, sticky=W)

    def sel1(self):
        self.cmd = self.var1.get()

    def load_it(self):
        self.master = Tk()
        self.e = Entry(self.master, width = 40)
        self.e.pack()
        b = Button(self.master, text = "OKAY", bg="black", foreground="red", command=self.input_it)
        b.pack()

    def color_out(self):
        row = len(self.row_col_dict["hor"])
        column = len(self.row_col_dict["ver"])

        for i in range(self.ver_con_size, column + self.ver_con_size):
            for j in range(self.hor_con_size, row + self.hor_con_size):
                w = Label(self.root, text='', bg='white', height=1, width=1)
                w.grid(row =i , column=j)

        self.root.update()

    def input_it(self):
        self.row_col_dict = ast.literal_eval(self.e.get())
        self.master.destroy()
        self.root.destroy()

        self.root = Tk()
        self.grid_dict = {}
        self.hor_con_size = find_max(self.row_col_dict["ver"])
        self.ver_con_size = find_max(self.row_col_dict["hor"])
        self.nono_grid = nonogrid_maker(self.root, self.row_col_dict, self.grid_dict)
        self.ver, self.hor = self.root.grid_size()

        self.panel_maker_1()

        self.cmd = ''

        self.note = ScrolledText(self.root, height=10, width=52)
        result = "%3s%8s%15s%14s\n" % ("Mode", " # SolvingTime /", " Assigned_VAR /", "# Pruned_VAR")

        self.note.insert(INSERT, result)
        self.note.insert(END, '----------------------------------------------------\n')
        self.note.configure(state=DISABLED)
        self.note.grid(row=4, column=self.ver+1, rowspan=10, columnspan=52)

        self.is_tracing_On = IntVar()
        self.tracing_cb = Checkbutton(self.root, text="Tracing Mode", variable=self.is_tracing_On)
        self.tracing_cb.grid(row=10, column=int(self.ver))

        self.solve_button = Button(self.root, text="SOLVE", bg="black", foreground="white", command = self.solve_it)
        self.solve_button.grid(row = 11, column = self.ver)
        self.save_button = Button(self.root, text="SAVE", bg="white", foreground = "red", command = self.out_it)
        self.save_button.grid(row = 14, column = self.ver)
        self.load_button = Button(self.root, text="LOAD", bg="white", foreground = "red", command = self.load_it)
        self.load_button.grid(row = 15, column = self.ver)
        self.quit_button = Button(self.root, text="Quit", bg="green", foreground="white", command=self.root.destroy)
        self.quit_button.grid(row = 18, column = self.ver)


def colour_in(root, result, grid_dict, vertical, horizontal):
    ver = vertical
    hor = horizontal
    inner_hor = 0

    for i in range(hor - len(result), hor):
        inner_ver = 0
        for j in range(ver - len(result[inner_ver]), ver):
            if result[inner_hor][inner_ver] == 1:
                w = Label(root, text='', bg='black', height=1, width=1)
                w.grid(row =i, column = j)
            if result[inner_hor][inner_ver] == 0:
                w = Label(root, text='', bg='white', height=1, width=1)
                w.grid(row=i, column=j)
            inner_ver = inner_ver + 1
        inner_hor = inner_hor + 1

    root.update()

def text_in(app, mode, assignedVar, solvingTime, PrunedVar):
    #var could be IT = iteration, TC = Time Complexity, NO = Nodes
    if mode is 1:
        mode_text ='MRV'
    elif mode is 2:
        mode_text = 'DH'
    elif mode is 4:
        mode_text = 'CST'
    else:
        mode_text = 'GAC'
    app.note.configure(state=NORMAL)
    if assignedVar >= 0 :
       result = "%4s:%11s%13s%15s\n" % (mode_text, str(assignedVar), str(solvingTime), str(PrunedVar))
    else :
        result = "Error : Please select the mode \n"
    app.note.insert(END, result)
    app.note.configure(state=DISABLED)


if __name__ == "__main__":
    cat = {'ver': [[1,1],[3],[5],[5],[1,1],[1,1],[2,2],[3,1],[5]],'hor':[[2],[4],[8],[4,3],[2,2],[1],[3],[3]]}
    app = Nonogram(cat)

    app.root.mainloop()

    # colour_in(app.root, result, app.grid_dict, app.ver, app.hor)
    # text_in(app, 2, 3, 4)
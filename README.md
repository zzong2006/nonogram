# Nonogram

![image-20200916192953165](https://i.loli.net/2020/09/16/FquIBmCZT4cptvL.png)

*WARNING: Unfortunately, when we tried to run the program under CSC domain an error was prompt regarding Tkinker that our project mainly depends on. However if ran under python versions above 2.7 our program seems to be able to run without such error. Hope you will understand .*
*(If you have the problem mentioned above, try to enter this command 'apt-get install python-tk' on your machine(s).)*

### Instruction

1. Access `nonogram.py` to start the program.
2. When ran, a window/game will be prompted

  * Originally, game is given a set of Nonogram constraint as an example
  * After choosing sorting algorithm by pressing one of the four radio-button and decide on 
    the option of "tracer", press solve button then a picture of kitty cat will reveal itself onto the grid
  * However user may choose to input set of the nonogram Constraint of its own by:

  1. Clicking `LOAD` button 

  2. When additional window gets prompted write down your desirable **constraints**.
      However, give the input in terms of nested list within a dictionary with dictionary key of `ver` and `hor` (`ver` indicating vertical constraints and `hor`   horizontal constraints)
    
    * Example
    
      ```python
      cat = {'ver': [[1,1],[3],[5],[5],[1,1],[1,1],[2,2],[3,1],[5]],'hor':[[2],[4],[8],[4,3],[2,2],[1],[3],[3]]}
      app = Nonogram(cat)
      app.root.mainloop()
      ```
    
      ,which results a grid that looks above image.

  3. Then just as you did to the original input, choose sorting algorithm, and the option of "Tracer" then press solve.

3. When the program finishes the solving, appropriate result will be shown on the text panel on side.
4. Whenever you would like to save the set of constraints you have inputted on `Load` for later use, press `Save` button then another window will be prompt with your previous input in it. Then copy the output onto separate notepad, word-file etc. for your convenient later use of the application.  
5. Whenever you would like to exit the game press the green `Quit` button


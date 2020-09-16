WARNING: Unfortunately when we tried to run the program under CSC domain an error was prompt 
regarding Tkinker that our project mainly depends on. However if ran under python versions above 2.7 our 
program seems to be able to run without such error. Hope you will understand .
(If you have the problem mentioned above, try to enter this command 'apt-get install python-tk' on your machine(s).)

1. Access nonogram.py to start the program 
2. When ran, a window/game will be prompted

	*Originally, game is given a set of Nonogram constraint as an example
	*After choosing sorting algorithm by pressing one of the four radiobutton and decide on 
	the option of "tracer", press solve button then a picture of citty cat will reveal itself onto the grid
	*However user may choose to input set of nonogram Constraint of its own by:

	1. Clicking "Load" button 
	2. When additional window gets prompted write down your desirable constraints.
	  However, give the input in terms of nested list within a dictionary 
	  with dictionary key of "ver" and "hor" ("ver" indicating vertical constraints and "hor" 
	  horizontal constraints)

	  ex. {"ver":[[1,2],[3,4,5]], "hor":[[6,7,8],[9,1]]}
	    Which results a grid that looks

		   3
		1 4
		2 5
       	       6 7 8- -  	
	         9 1- -

	3. Then just as you did to the original input, choose sorting algorithm,
	  and the option of "Tracer" then press solve 
	4. When finish solving approprite result will be shown on the text panel on side 
	5. Whenever you would like to save the set of constraints you have inputted on "Load"
	  for later use, press "Save" button then another window will be prompt with your 
	  previous input in it. Then copy the output onto seperate notepad, wordfile etc.
	  for your convinent later use of the application.  
	6. Whenever you would like to exit the game press "Quit" button
# AI_Homework
Homework Assignments completed for Artificial Intelligence Class (Coen 266)

Please note that many of the files in this repository were provided to me by the lecturer of the class.
All files written by my have a header at the top which states so.

Descriptions:
hw1:
  We were tasked in implementing an A* search algorithm, and a Bidirectional Breadth First Search algorithm for extra credit.
hw2:
  Tasked in making a propositional logic resolution-based inference engine
hw3:
  Had to implement a decision tree model using the ID3 algorithm for creating the tree. Random forest for extra credit
  
Running:
hw1:
  ./main.py astar.py tests/astar-1-jconner.map
  This runs the astar implemented search, you can change the test maps to run it on as well (ie tests/astar-2-jconner.map)
  
  ./main.py bbfs.py tests/astar-4-jconner.map
  This runs the bidirectional breadth first search.
 
h2:
  execute files under tests/ that start with filename 'simple'
  
h3:
  run the following command
  python2 ./main.py id3 white-can-win --attributes tests/kr-vs-kp-attributes.txt \
--train tests/kr-vs-kp-train.csv --test tests/kr-vs-kp-test.csv

  Change the file names to others in the folders for different cases. 
  Also you can comment line 24 in id3.py to get rid of the huge print statement.
  note that this has to be run in python2

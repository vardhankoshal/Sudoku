# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The Naked Twin strategy can only be applied when we have boxes with just 2 digits 
as possible values. By making Naked Search technique as part of reduce_puzzle constraint propagation, along with eliminate and only choice techniques, 
the algorithm can further reduce the number of unsolved boxes with 2 possible values with help of naked twin strategy before moving to search.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We used constraint propogation as reduce_puzzle method in form of loop with eliminate and only choice techniques applied repeatedly on the sudoku puzzle.
By including diagonals as units and adding them to the existing unit list that we use fo implement eliminate and only choice, the constraint is
automatically included in the reduce_puzzle function, hence providing the solution to the diagonal puzzles as well wherever possible.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
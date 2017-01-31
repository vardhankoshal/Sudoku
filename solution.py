import itertools
assignments = []

def assign_value(values, box, value):
    # type: (object, object, object) -> object
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
        Keys: The boxes, e.g., 'A1'
        Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


#Creating iterables for usage in functions below

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#For solving diagonal Sudokus, we will need 2 more units along the diagonal of the puzzle
diagonal1 = [rows[i]+cols[i] for i in range(9)]
diagonal2 = [rows[i]+cols[8-i] for i in range(9)]
diag_units = [diagonal1, diagonal2]


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values:
        width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                          for c in cols))
        if r in 'CF': print(line)




def eliminate(values):
    """
    This is the implementation of the most fundamental rule of solving Sudoku: Not to have any digit twice in a unit.
    A unit is defined as either a column, a row or a square of 9 boxes.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values




def naked_twins(values):
    """Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}

        Returns:
            the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
      unit_dict = dict((s, values[s]) for s in unit) #creating a sub-dictionary for this unit
      x={} #counting number of instances of all values in this unit
      for v in unit_dict.values():
        if not v in x: x[v]=1
        else: x[v]+=1
      twins = [a for a in x if x[a] == 2 and len(a) == 2] #the list of values of twins present in this unit
      if len(twins) > 0:
        for t in twins:
         for u in unit_dict:
          if unit_dict[u] != t:
              assign_value(values, u, values[u].replace(t[0], '')) #eliminating the first digit of twins from all unit peers
              assign_value(values, u, values[u].replace(t[1], '')) #eliminating the second digit of twins from all unit peers
    return values




def hidden_twins(values):
    """Adding a more generic twin strategy called Hidden Twins strategy,
    where we identify the twin pairs among boxes with any number of
    possible values and not just those with just 2 possible values"""
    tv = list(itertools.combinations('123456789', 2))#creating a list of all 2 digit pairs except those with same digits
    tv.sort() #Sorting them in increasing order
    tv_dict = dict((x, 0) for x in tv) #creating a counter dictionary for all 2 digit pairs ('12'-'98')inside a unit and initializing it with 0 for all
    for unit in unitlist:
        unit_dict = dict((s, values[s]) for s in unit) #creating a sub-dictionary for this unit
        for t in list(tv): #iterating for all 2 digit pairs
            for v in unit_dict.values():
                if not t in itertools.combinations(v, 2): tv_dict[v]=0
                else: tv_dict[t]+=1
                twins = [a for a in tv_dict if tv_dict[a] == 2] #the list of values of double digit twins present in this unit
                if len(twins) > 0:
                    for t in twins:
                        for u in unit_dict:
                            if unit_dict[u] != t:
                                assign_value(values, u, values[u].replace(t[0], '')) #eliminating the first digit of twins from all unit peers
                                assign_value(values, u, values[u].replace(t[1], '')) #eliminating the second digit of twins from all unit peers
                return values


def reduce_puzzle(values):
    """
    Here we reduce the given sudoku puzzle using successive iterations of elimination and only-choice methods.
    This process can solve easy puzzles completely.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)  #Adding naked twins strategy here, though not required now because of more generic hidden twin strategy being added below
        values = hidden_twins(values) #Adding hidden twins strategy here
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print("Error: Sudoku not solvable due to incorrect values")
            return False
    return values



def search(values):
    """
    After reducing the puzzle to best possible state using reduce_puzzle(), we then use search method to see the solution
    that can be obtained by considering a particular value assigned to the box from the list of possible values,
    using depth first search and recursive application.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid, is_diagonal = True):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Converting sudoku string into a dictionary
    sudoku = grid_values(grid)
    #Solving for diagonal condition by including 2 diagonals in list of units
    if is_diagonal:
        global unitlist
        unitlist = unitlist + diag_units
        sudoku_d = search(sudoku)
        if not sudoku_d:
            print("Not solvable for diagonal")
            return(False)
        else:
            return sudoku_d
    else:
        return search(sudoku)



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

# A Sudoku solver

This is a sudoku solver inspired by [this youtube video][1] but with classes
and strings as the sudoku representation.

## Run it

To run it, simply start run.py with a recent python interpreter
(tested with python 3.7 and 3.8).

```sh
python ./run.py
```

## Define a puzzle

If you want to define a new puzzle, you need to redefine the *game* variable
in run.py's *main* function. This is simply one long string which is split up
into rows for better readability.

```python
game = (
    "....54.6."
    "167.2...."
    "..5..18.3"
    # ---------
    ".8.4....9"
    "..16934.."
    "3....5.1."
    # ---------
    "4.82..1.."
    "....8.594"
    ".1.54...."
)
```

## Not implemented yet

* Puzzle input from cli or text file

[1]: https://www.youtube.com/watch?v=G_UYXzGuqvM

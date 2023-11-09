'''
  Byimaan
  - Subhpreet Singh (https://github.com/SubhPB/)

  last updated - Nov 8, 2023
'''

from sympy import simplify
import math
from sympy.abc import x, y, z
from sympy import pprint, Eq, solve, integrate

'''
Why we need this class. 
because default solve(Eq(..),(var..) returns the result in different data type
sometimes it return the result in dict and sometimes in list according to the complexity of
the equation and number of variables in the equation that's why in order to find the critical
points we need a single data-type of results all the time...   - Thanks
'''

class Equation:
    """
    This class represents an equation using sympy's Eq object.
    """
    def __init__(self, equation: Eq):
        """
        Initialize the Equation object with a sympy Eq object.
        """
        if not isinstance(equation, Eq):
            raise TypeError('''
            The given data type for equation is not valid. The equation should be the instance of sympy.core.relational.Equality
            ''')

        self.equation = equation
        # Determine the number of variables in the equation
        self.no_of_vars = len(set(equation.free_symbols))

    def __str__(self):
        """
        Return a string representation of the order of the equation based on the number of variables.
        """
        return f"order = {self.no_of_vars}"

    def __call__(self, *args, **kwargs):
        """
        When an instance of Equation is called, return the equation itself.
        """
        return self.equation

class EquationSolver:
    """
    This class solves a system of equations provided as a list of Equation instances.
    """
    def __init__(self, equations_list):
        """
        Initialize the EquationSolver with a list of Equation objects.
        """
        if not isinstance(equations_list, list) and all(isinstance(i, Equation) for i in equations_list):
            raise ValueError('''
            The equation should be instance of Eq and all equations should be zipped in a list
            ''')

        self.eq_list = equations_list
        # Find the highest order of the equations in the list
        self.highest_order = max([eq.no_of_vars for eq in equations_list])

    def __call__(self, *args, **kwargs):
        """
        Solve the system of equations when the instance is called.
        """
        container = []

        try:
            # Solve the system and handle the solution appropriately
            solution = solve((i() for i in self.eq_list), (x, y, z))

            if isinstance(solution, dict):
                # If the solution is a dictionary, append it to the container
                container.append(solution)

            if isinstance(solution, list):
                # Handle a list of solutions based on their length and organize them into dictionaries
                for i in solution:
                    if len(i) == 3:
                        container.append({'x': i[0], 'y': i[1], 'z': i[2]})
                    if len(i) == 2:
                        container.append({'x': i[0], 'y': i[1]})
                    if len(i) == 1:
                        container.append({'x': i})

        except:
            raise ValueError('''
            Something went wrong!
            ''')

        finally:
            return container

if __name__ == "__main__":
    # Example system of equations
    e4 = Eq(x*2 + y + z, 2)
    e5 = Eq(3 * x + 5 * y + 3*z, 8)
    e6 = Eq(6 * x - 4 * y + z, 4)

    # Create a list of Equation objects
    l = [Equation(e4), Equation(e5), Equation(e6)]

    # Solve the system and print the result
    pprint(EquationSolver(l)())

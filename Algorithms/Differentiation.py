'''
  Byimaan
  - Subhpreet Singh (https://github.com/SubhPB/)

  last updated - Nov 8, 2023
'''

import sympy
from sympy import simplify
import math
from sympy.abc import x, y, z  # Importing symbolic variables for differentiation
from sympy import pprint, Eq, solve, integrate
from Equations import Equation, EquationSolver  # Assuming Equation and EquationSolver are defined in another module

class Differentiation:
    """
    This class is for performing symbolic differentiation on an expression with respect to a given symbol.
    """
    def __init__(self, expression, symbol):
        """
        Initialize the Differentiation object with an expression and symbol for differentiation.
        """
        # Ensure the symbol is a sympy Symbol object
        if isinstance(symbol, sympy.core.symbol.Symbol):
            symbol = sympy.symbols(str(symbol))

        self.expression = expression
        self.symbol = symbol

    def differentiate(self, values=0):
        """
        Perform differentiation on the expression. If values are provided, evaluate the derivative at those values.
        """
        try:
            if values:
                try:
                    return sympy.diff(self.expression, self.symbol).subs(values)
                except:
                    return sympy.diff(self.expression, self.symbol)
            return sympy.diff(self.expression, self.symbol)
        except Exception as e:
            print("- Differentiation was not successful! ")
            return e

    def nth_differentiation(self, n):
        """
        Perform n-th order differentiation on the expression.
        """
        if not isinstance(n, int) and n > 0:
            raise TypeError(f'''
            Wrong value for n, n supposed to be an integer and should be > 0
            ''')

        if n == 1:
            return self.differentiate()

        self.expression = self.differentiate()

        return self.nth_differentiation(n - 1) if self.expression != 0 else 0

    def mixed_partial_differentiation(self, order_of_symbols):
        """
        Perform mixed partial differentiation on the expression based on the order of symbols provided.
        """
        if not isinstance(order_of_symbols, list) and order_of_symbols < 1:
            raise TypeError('''
            Order of symbols needs to be in list form - like -> [x,y,z] and length should be greater than 1.
            ''')

        if not all(isinstance(i, sympy.core.symbol.Symbol) for i in order_of_symbols):
            raise TypeError(f'''
            All variables should be the instance of sympy.core.symbol.Symbol but got {type(order_of_symbols[0])} 
            ''')

        self.symbol = order_of_symbols[0]

        self.expression = self.differentiate()

        if len(order_of_symbols) == 1:
            return self.expression

        return self.mixed_partial_differentiation(order_of_symbols[1:]) if self.expression != 0 else 0


class Second_derivative_test:
    """
    This class is used to perform the second derivative test to classify critical points.
    """
    def __init__(self, expression, critical_points=None):
        """
        Initialize the Second_derivative_test object with an expression and critical points.
        """
        if not all(isinstance(i, dict) for i in critical_points) and not isinstance(critical_points, list):
            raise TypeError('Type Error critical point should look like -> [{"x":1,"y":2}]')

        if len(critical_points) == 0:
            raise ValueError(f"Got empty critical points. Critical points are needed to execute this code.")

        self.expression = expression
        self.ck_p = critical_points

    def __call__(self, *args, **kwargs):
        """
        Execute the second derivative test when the object is called.
        """
        value = {"local_min": {}, "local_max": {}, "saddle_point": {}, "inclusive_point": {}}

        try:
            for i in self.ck_p:
                # Based on the second derivative test, classify the critical points
                if (self.Fxx().subs(i) > 0 and self.determinant().subs(i) > 0):
                    value["local_min"] = self.ck_p

                elif (self.Fxx().subs(i) < 0 and self.determinant().subs(i) > 0):
                    value["local_max"] = self.ck_p

                elif (self.determinant().subs(i) < 0):
                    value["saddle_point"] = self.ck_p

                elif(self.determinant().subs(i) == 0):
                    value["inclusive_point"] = self.ck_p

                else:
                    print('''
                    Got Unexpected Answer. Function not successful...
                    ''')
                    return

                return value

        except:
            print('''
            Got Unexpected Answer. Function not successful.
            More code is needed to get the answer. Thanks
            ''')
            return

    def Fxx(self):
        """
        Calculate the second partial derivative with respect to x.
        """
        diff = Differentiation(self.expression, x)

        try:
            return simplify(diff.nth_differentiation(2))
        except:
            return diff.nth_differentiation(2)

    def Fxy(self):
        """
        Calculate the mixed second partial derivative with respect to x and y.
        """
        diff = Differentiation(self.expression, x)

        fxx = diff.differentiate()

        fxy = Differentiation(fxx, y)

        try:
            return simplify(fxy.differentiate())
        except:
            return fxy.differentiate()

    def Fyy(self):
        """
        Calculate the second partial derivative with respect to y.
        """
        diff = Differentiation(self.expression, y)

        try:
            return simplify(diff.nth_differentiation(2))
        except:
            return diff.nth_differentiation(2)

    def determinant(self):
        """
        Calculate the determinant of the Hessian matrix.
        """
        try:
            return simplify(self.Fxx() * self.Fyy() - (self.Fxy()) ** 2)
        except:
            return self.Fxx() * self.Fyy() - (self.Fxy()) ** 2

class Absolute_Values:
    """
    This class finds the absolute maximum and minimum values of an expression over a set of critical points.
    """

    def __init__(self, expression, critical_points):
        """
        Initialize the Absolute_Values object with an expression and critical points.
        """
        if not all(isinstance(i, dict) for i in critical_points) and not isinstance(critical_points, list):
            raise TypeError('Type Error critical point should look like -> [{"x":1,"y":2}]')

        if len(critical_points) == 0:
            raise ValueError(f"Got empty critical points. Critical points are needed to execute this code.")

        self.expression = expression
        self.ck_points = critical_points

    def __call__(self):
        """
        Execute the process to find absolute maxima and minima when the object is called.
        """
        extreme_values = {'absolute_max': {}, 'absolute_min': {}}

        maximum = -math.inf
        minimum = math.inf

        for i in self.ck_points:
            val = simplify(self.expression.subs(i)) if not isinstance(self.expression,
                                                                      (int, float)) else self.expression

            if val > maximum:
                maximum = val
                extreme_values['absolute_max'] = maximum

            if val <= minimum:
                minimum = val
                extreme_values['absolute_min'] = minimum

        return extreme_values

class FindCriticalPoints:
    """
    This class is used to find the critical points of an expression.
    """

    def __init__(self, expression, point=None):
        """
        Initialize the FindCriticalPoints object with an expression and optionally a specific point.
        """
        if point:
            if not isinstance(point, dict):
                raise TypeError(f'''
                Parameter - point got wrong data type supposed to be a dict. But got {type(point)}
                ''')

        self.expression = expression
        self.point = point

    def __call__(self, *args, **kwargs):
        """
        Execute the process to find critical points when the object is called.
        """
        # Find the partial derivatives with respect to x, y, and z
        f_x = Differentiation(self.expression, x).differentiate()
        f_y = Differentiation(self.expression, y).differentiate()
        f_z = Differentiation(self.expression, z).differentiate()

        # Equate the partial derivatives to zero to find critical points
        e1 = Eq(f_x, 0) if f_x != 0 else None
        e2 = Eq(f_y, 0) if f_y != 0 else None
        e3 = Eq(f_z, 0) if f_z != 0 else None

        try:
            # Solve the system of equations to find the critical points
            l = [Equation(e) for e in (e1, e2, e3) if e != None]

            critical_points = EquationSolver(l)()

            return critical_points

        except:
            print("Something went wrong during the execution with Equation Class")
            raise Exception

if __name__ == "__main__":
    # Example usage of the classes defined above
    expression = 140 * x + 180 * y - 3 * x ** 2 - 2 * y ** 2 - x * y

    # Find critical points for the given expression
    critical_points = FindCriticalPoints(expression)()
    pprint(critical_points)

    # Find the derivative with respect to y
    pprint(Differentiation(expression, y).differentiate())

    # Find absolute values at the critical points
    absolute_values = Absolute_Values(expression, critical_points)()
    #
    local = Second_derivative_test(expression, critical_points)()
    #
    print(local)


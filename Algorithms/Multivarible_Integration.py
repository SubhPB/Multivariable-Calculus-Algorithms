'''
  Byimaan
  - Subhpreet Singh (https://github.com/SubhPB/)

  last updated - Nov 9, 2023
'''

import sympy as sy
import math
from sympy.abc import x, y, z, r, theta
from sympy import simplify,pprint, Eq, solve, integrate
import itertools

class MultivariableIntegration:
    # This class is designed to handle various types of multivariable integrations

    def get_integration(self, expression, sym):
        # Function to perform integration of a given expression with respect to a symbol 'sym'
        ans = integrate(expression, sym)  # Performing the integration
        try:
            ans = simplify(ans)  # Attempting to simplify the result of the integration
        except:
            print("An exception occurred... ")
            pass
        return ans  # Returning the possibly simplified integral

    def find_integration_with_limits(self, expression, sym, limit):
        # Function to perform definite integration with specified limits
        if not (isinstance(limit, dict)):
            # Checking if the limit is provided in the correct dictionary format
            print('''
                 limit should be well formatted 
                 example - limit = {"a" : 5, "b" : 7} 
            ''')
            return

        answer = self.get_integration(expression, sym)  # Performing indefinite integration

        try:
            # Calculating the definite integral by substituting the upper and lower limits
            return simplify(answer.subs({f"{sym}": limit["b"]}) - answer.subs({f"{sym}": limit["a"]}))
        except:
            # In case of an exception, return the difference without simplification
            return answer.subs({f"{sym}": limit["b"]}) - answer.subs({f"{sym}": limit["a"]})

    def solve_multiple_integral(self, expression, limit):
        # Function to handle the integration of multiple variables
        if not (isinstance(limit, list) and all(isinstance(item, dict) for item in limit)):
            # Checking if limits are provided in the correct format
            print('''
                 limit should be well formatted 
                 example - limit = [{"x" : {"a":0,"b":5}} , {"y" : {"a":0,"b":7}}, ... ]
            ''')
            return

        if len(limit) == 0:
            # If no limits are provided, return the original expression
            return expression

        # Perform the integration for the first variable in the list
        integration = self.find_integration_with_limits(expression, eval(list(limit[0].keys())[0]), list(limit[0].values())[0])

        # Recursively solve the remaining integrals
        return self.solve_multiple_integral(integration, limit[1:])


if __name__ == "__main__":
    '''
    When dealing with trignometry use sympy rather than 'math' library 
    '''

    solve = MultivariableIntegration()

    expression = x**2 + sy.sin(y)/2 + z*2

    limit = [{"x":{"a":0,"b":3}},{"y":{"a":2,"b":sy.pi}},{"z":{"a":1,"b":4}}]

    try:

       answer = solve.solve_multiple_integral(expression,limit)
       pprint(answer)

    except:
        print(" Something went wrong!. Please ensure you gave the valid input.")
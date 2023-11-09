'''
  Byimaan
  - Subhpreet Singh (https://github.com/SubhPB/)

  last updated - Nov 8, 2023
'''
import sympy
from sympy import simplify
import math
from sympy.abc import x, y, z, l, L
from sympy import pprint, Eq, solve, integrate
from Differentiation import Differentiation

class MetaClass(type):
    """
    (Optional Feature - if you want to reduce the repetition of some lines of code)
    This is a metaclass used to enforce certain checks before creating instances of classes.
    However, i did not implement it in any class as parent just to make the things simple
    """
    def __call__(cls, *args, **kwargs):
        """
        Enforce that the second argument (args[1]) is a dictionary. This is likely used in subclasses.
        """
        if not isinstance(args[1], dict):
            raise ValueError(f'''
            Parameter - point got wrong data type supposed to be a dict. But got {type(args[1])}
            ''')

        return super().__call__(*args, **kwargs)

class Vector:
    """
    This class represents a mathematical vector with three components (x, y, z).
    """
    def __init__(self, x=0, y=0, z=0):
        """
        Initialize the vector with x, y, and z components.
        """
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        """
        String representation of the vector, simplifying the components if possible.
        """
        try:
            c_x, c_y, c_z = simplify(self.x), simplify(self.y), simplify(self.z)
        except:
            c_x, c_y, c_z = self.x, self.y, self.z

        return f"{c_x, c_y, c_z}"

    def __call__(self, *args, **kwargs):
        """
        When an instance is called, return a list of its components.
        """
        return [self.x, self.y, self.z]

    def __add__(self, other):
        """
        Define addition for two Vector instances.
        """
        if isinstance(other, Vector):
            # Add corresponding components of the two vectors
            return Vector(*(list(map(lambda i, j: i + j, self(), other()))))

        raise ValueError(f'''
        The following operation is not valid for the given data type ({type(other)}). It is supposed to be a type of Vector
        ''')

    def __sub__(self, other):
        """
        Define subtraction for two Vector instances.
        """
        if isinstance(other, Vector):
            # Subtract corresponding components of the two vectors
            return Vector(*(list(map(lambda i, j: i - j, self(), other()))))

        raise ValueError(f'''
        The following operation is not valid for the given data type ({type(other)}). It is supposed to be a type of Vector
        ''')

    def __mul__(self, other):
        """
        Define multiplication for a Vector instance with either another Vector or a scalar.
        """
        if isinstance(other, Vector):
            # Multiply corresponding components of the two vectors
            return Vector(*(list(map(lambda i, j: i * j, self(), other()))))

        # Check if 'other' is a scalar (int, float, or various sympy number types)
        if isinstance(other,
                      (
                           int, float, sympy.core.symbol.Symbol,
                           sympy.core.numbers.Integer, sympy.core.numbers.Float,
                           sympy.core.numbers.Rational, sympy.core.mul.Mul
                      )
                     ):
            # Multiply each component of the vector by the scalar
            return Vector(*(list(map(lambda i: i * other, self()))))

        raise ValueError(f'''
        The following operation is not valid for the given data type ({type(other)}). It is supposed to be a type of Vector
        ''')

    def unit_vector(self):
        """
        Calculate and return the unit vector in the direction of this vector.
        """
        # Calculate the magnitude of the vector
        sqrt = sympy.sqrt(sum([i**2 for i in self()]))

        try:
            # Divide each component of the vector by its magnitude
            return self * (1 / sqrt)
        except:
            raise TypeError('''
            Something went wrong in finding out the unit vector
            ''')

class FindGradient:
    """
    This class is used for finding the gradient of a given mathematical expression.
    """
    def __init__(self, expression, point=None):
        """
        Initialize with an expression. 'point' is optional and used for evaluating the gradient at a specific point.
        """
        self.expression = expression
        self.point = point

    def __call__(self, *args, **kwargs):
        """
        Calculate the gradient of the expression. This is done by differentiating the expression with respect to x, y, and z.
        """
        # Differentiate the expression with respect to x, y, and z.
        diffx = Differentiation(self.expression, x)
        diffy = Differentiation(self.expression, y)
        diffz = Differentiation(self.expression, z)

        # Get the differentiated components.
        x_component = diffx.differentiate()
        y_component = diffy.differentiate()
        z_component = diffz.differentiate()

        # If a point is provided, substitute it into the components.
        if self.point:
            try:
                return Vector(x_component.subs(self.point), y_component.subs(self.point), z_component.subs(self.point))
            except:
                return Vector(x_component, y_component, z_component)

        vector = Vector(x_component, y_component, z_component)
        return vector

    def find_direction(self, point):
        """
        Find the direction of steepest ascent at a given point.
        """
        if not isinstance(point, dict):
            raise TypeError(f'''
            Parameter - point got wrong data type supposed to be a dict. But got {type(point)}
            ''')
        try:
            v = self() * self()
            try:
               mod = sympy.sqrt(sum(v())).subs(point)
            except:
                mod = sympy.sqrt(sum(v()))
            return mod
        except Exception as exc:
            raise exc

class FindUnitNormalVector:
    """
    This class is for finding the unit normal vector at a given point on the surface defined by an expression.
    """
    def __init__(self, expression, point):
        """
        Initialize with an expression and a point.
        """
        if not isinstance(point, dict):
            raise TypeError(f'''
            Parameter - point got wrong data type supposed to be a dict. But got {type(point)}
            ''')
        self.expression = expression
        self.point = point

    def __call__(self, *args, **kwargs):
        """
        Calculate the unit normal vector.
        """
        g = FindGradient(expression=self.expression)

        # Get the gradient vector
        get_gradient = g()

        try:
            # Calculate the magnitude of the gradient vector
            sqrt = math.sqrt(sum([i.subs(self.point)**2 if not isinstance(i, int or float) else i for i in get_gradient()]))
        except:
            # If the above fails (likely due to symbolic variables), use sympy's sqrt
            sqrt = sympy.sqrt(sum([i.subs(self.point)**2 if not isinstance(i, int or float) else i  for i in get_gradient()]))

        components = []

        # Normalize each component of the gradient vector to get the unit normal vector
        for item in get_gradient():
            components.append(item.subs(self.point) / sqrt)

        return Vector(*components)

class TangentPlane:
    def __init__(self, expression, point):
        """
        Initialize with an expression representing a surface and a point.
        """
        if not isinstance(point, dict):
            raise TypeError(f'''
            Parameter - point got wrong data type supposed to be a dict. But got {type(point)}
            ''')

        self.expression = expression
        self.point = point

    def __call__(self, *args, **kwargs):
        """
        Calculate the equation of the tangent plane at a given point.
        """
        vector = Vector(x, y, z)

        # Differentiating the expression with respect to x, y, and z.
        diffx = Differentiation(self.expression, x).differentiate(self.point)
        diffy = Differentiation(self.expression, y).differentiate(self.point)
        diffz = Differentiation(self.expression, z).differentiate(self.point)

        equation = [vector.x - self.point['x'], vector.y - self.point['y'], vector.z - self.point['z']]

        try:
            return simplify(diffx * equation[0] + diffy * equation[1] + diffz * equation[2])
        except:
            return diffx * equation[0] + diffy * equation[1] + diffz * equation[2]

    def linear_approximation(self, approx_point=0):
        """
        Perform a linear approximation of the function at a given point.
        """
        func = self.expression.subs(self.point) if not isinstance(self.expression, (int, float)) else self.expression

        try:
            if approx_point:
               pprint(func)
               return (self(self.expression, self.point)() + func).subs(approx_point)
            raise ValueError('Something went wrong! ')
        except:
            return TangentPlane(self.expression, self.point)() + func

class DirectionalDerivative():
    def __init__(self, expression, point, vector=Vector, angle=None):
        """
        Initialize with an expression, a point, a vector, and optionally an angle.
        """
        if not isinstance(vector, Vector):
            raise TypeError(f'''
            Parameter - point got wrong data type supposed to be a vector. But got {type(point)}
            ''')

        self.expression = expression
        self.vector = vector if not angle else Vector(sympy.cos(angle), sympy.sin(angle))
        self.point = point

    def __call__(self):
        """
        Calculate the directional derivative.
        """
        # Differentiating the expression with respect to x, y, and z.
        diffx = Differentiation(self.expression, x).differentiate(self.point)
        diffy = Differentiation(self.expression, y).differentiate(self.point)
        diffz = Differentiation(self.expression, z).differentiate(self.point)

        diff_vector = Vector(diffx, diffy, diffz)

        # Calculating the dot product of the gradient vector and the unit vector in the given direction.
        v = diff_vector * self.vector.unit_vector()

        try:
            return simplify(sum(v()))
        except:
            return sum(v())


if __name__ == "__main__":
    #maximim rate of change -> steepest_direction()

    point = {'x':4,'y':1,'z':0}
    expr = 3*x*sympy.sin(x*y)

    v = Vector(5,-6)

    pprint(FindGradient(expr).find_direction(point))


import sympy as sp
import re

def simplify_powers(expr):
    # Add debug prints 
    print("DEBUG: Expression type:", type(expr))
    print("DEBUG: Expression:", expr)
    if hasattr(expr, "args"):
        print("DEBUG: Args:", expr.args)
    if hasattr(expr, "exp"):
        print("DEBUG: Exponent:", expr.exp)
    if hasattr(expr, "base"):
        print("DEBUG: Base:", expr.base)

    # Look for sqrt(x**2) -> x pattern
    if isinstance(expr, sp.Pow) and expr.exp == sp.Rational(1, 2):  # sqrt
        if isinstance(expr.base, sp.Pow) and expr.base.exp == 2:
            return expr.base.base  # sqrt(x**2) -> x
    
    # The other direction (sqrt(x)**2 -> x) seems to be handled automatically by sympy
    
    # Recurse through the expression tree
    if hasattr(expr, 'args') and len(expr.args) > 0:
        return expr.func(*[algebra.simplify_powers(arg) for arg in expr.args])
    return expr


def minimal_simplify(equation):
    print("\nOriginal equation:", equation)
    try:
        # Basic expansion
        lhs = sp.expand(equation.lhs)
        rhs = sp.expand(equation.rhs)
        print("After expansion:", sp.Eq(lhs, rhs))

        # Try sympy's built-in powsimp function first
        lhs = sp.powsimp(lhs)
        rhs = sp.powsimp(rhs)
        
        # Apply power simplifications
        lhs = simplify_powers(lhs)
        rhs = simplify_powers(rhs)
        print("After power simplification:", sp.Eq(lhs, rhs))
        
        return sp.Eq(lhs, rhs)
    except Exception as e:
        print("ERROR:", e)
        return equation

# Test cases
def run_tests():
    x = sp.symbols('x')
    y = sp.symbols('y')
    
    # Case 1: sqrt(x²)
    print("\n--- TEST CASE 1: sqrt(x²) ---")
    test1 = sp.sqrt(x**2)
    print("Original:", test1)
    result1 = simplify_powers(test1)
    print("Result:", result1)
    
    # Case 2: (sqrt(x))²
    print("\n--- TEST CASE 2: (sqrt(x))² ---")
    test2 = (sp.sqrt(x))**2
    print("Original:", test2)
    result2 = simplify_powers(test2)
    print("Result:", result2)
    
    # Case 3: In equation - y = sqrt(x²)
    print("\n--- TEST CASE 3: y = sqrt(x²) ---")
    eq1 = sp.Eq(y, sp.sqrt(x**2))
    result_eq1 = minimal_simplify(eq1)
    
    # Case 4: In equation - y = (sqrt(x))²
    print("\n--- TEST CASE 4: y = (sqrt(x))² ---")
    eq2 = sp.Eq(y, (sp.sqrt(x))**2)
    result_eq2 = minimal_simplify(eq2)

if __name__ == "__main__":
    run_tests()
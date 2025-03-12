import streamlit as st
import random
import sympy as sp
from sympy import symbols, Eq, solve, sqrt, Pow, sympify, expand
import re

def latex_equation(equation):
    """Convert a sympy equation to a LaTeX string with some custom formatting"""
    # Convert to standard LaTeX
    latex_str = sp.latex(equation)
    
    # Add custom formatting for better display
    # Replace decimal powers with roots when possible
    latex_str = re.sub(r'\^\{0\.5\}', r'^{\\frac{1}{2}}', latex_str)
    
    return latex_str

def count_operations(expr):
    """Count the number of operations in an expression - used for complexity"""
    if isinstance(expr, sp.Eq):
        return count_operations(expr.lhs) + count_operations(expr.rhs)
    
    if expr.is_Add or expr.is_Mul:
        return sum(count_operations(arg) for arg in expr.args) + len(expr.args) - 1
    
    if expr.is_Pow:
        return count_operations(expr.base) + count_operations(expr.exp) + 1
    
    if isinstance(expr, sp.Pow) and expr.exp == 0.5:  # sqrt
        return count_operations(expr.base) + 1
        
    return 0  # Atomic expression (symbol or number)

def generate_equation(difficulty):
    """Generate a random algebra equation with a pedagogically sound solution path"""
    # Define difficulty parameters
    if difficulty == 'easy':
        num_steps = 2
        operations = ['add', 'sub', 'mul', 'div']
        max_value = 5
    elif difficulty == 'medium':
        num_steps = 3
        operations = ['add', 'sub', 'mul', 'div']
        max_value = 8
    elif difficulty == 'hard':
        num_steps = 3
        operations = ['add', 'sub', 'mul', 'div', 'sqr']
        max_value = 10
    else:  # extra_hard
        num_steps = 4
        operations = ['add', 'sub', 'mul', 'div', 'sqr', 'sqrt']
        max_value = 12
    
    # Choose target variable
    variables = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
    var_target = random.choice(variables)
    var_solve = random.choice([v for v in variables if v != var_target])
    
    # Start with the target variable
    target_sym = sp.symbols(var_target)
    solve_sym = sp.symbols(var_solve)
    
    # Begin with the simplest equation: solve_var = target_var
    current_expr = target_sym
    
    # Build the solution path by applying random operations
    solution_path = []
    final_operations = []
    
    # Operation functions and their inverses
    op_funcs = {
        'add': (lambda x, v: x + v, 'Subtract', lambda x, v: x - v),
        'sub': (lambda x, v: x - v, 'Add', lambda x, v: x + v),
        'mul': (lambda x, v: x * v, 'Divide by', lambda x, v: x / v),
        'div': (lambda x, v: x / v, 'Multiply by', lambda x, v: x * v),
        'sqr': (lambda x, v: x ** 2, 'Take the square root', lambda x, v: sp.sqrt(x)),
        'sqrt': (lambda x, v: sp.sqrt(x), 'Square it', lambda x, v: x ** 2),
    }
    
    # Avoid consecutive inverse operations
    inverse_pairs = {
        'add': 'sub', 'sub': 'add',
        'mul': 'div', 'div': 'mul',
        'sqr': 'sqrt', 'sqrt': 'sqr'
    }
    
    prev_op = None
    
    for _ in range(num_steps):
        # Choose an operation (avoiding inverse of the previous one)
        available_ops = [op for op in operations if op != inverse_pairs.get(prev_op, None)]
        if not available_ops:
            available_ops = operations.copy()
        
        op_name = random.choice(available_ops)
        prev_op = op_name
        
        # Choose a value for the operation
        if op_name in ['sqr', 'sqrt']:
            value = None
        else:
            # For division, avoid values that make fractions too complex
            if op_name == 'div':
                value = random.choice([2, 3, 4, 5])
            else:
                value = random.randint(2, max_value)
        
        # Get the forward operation function
        op_func, inverse_name, inverse_func = op_funcs[op_name]
        
        # Apply the operation to our expression
        if value is None:
            current_expr = op_func(current_expr, None)
        else:
            current_expr = op_func(current_expr, value)
        
        # Store the inverse operation for the solution path
        solution_path.append({
            'operation': inverse_name,
            'value': value
        })
        
        # Store the forward operation for display
        final_operations.append({
            'operation': op_name,
            'value': value
        })
    
    # Create the final equation
    final_equation = sp.Eq(solve_sym, current_expr)
    
    # Now create a proper solution path in reverse
    solution_steps = []
    for step in reversed(solution_path):
        solution_steps.append(step)
    
    return {
        'equation': final_equation,
        'target_var': var_target,
        'solve_var': var_solve,
        'solution_steps': solution_steps,
        'operations_applied': final_operations,
        'steps_taken': [],
        'current_state': final_equation,
        'original_equation': final_equation,
    }

def analyze_equation_state(equation, target_var):
    """Analyze the current state of the equation to determine hint suggestions"""
    target = sp.symbols(target_var)
    lhs, rhs = equation.args
    
    # Check where the target variable appears
    target_in_lhs = target in lhs.free_symbols
    target_in_rhs = target in rhs.free_symbols
    
    # Count occurrences
    target_count_lhs = str(lhs).count(target_var)
    target_count_rhs = str(rhs).count(target_var)
    
    # Analyze the structure
    analysis = {
        'target_alone': False,
        'target_almost_alone': False,
        'target_on_both_sides': target_in_lhs and target_in_rhs,
        'target_on_left': target_in_lhs,
        'target_on_right': target_in_rhs,
        'has_addition': '+' in str(equation),
        'has_subtraction': '-' in str(equation),
        'has_multiplication': '*' in str(equation),
        'has_division': '/' in str(equation),
        'has_power': '**' in str(equation) or 'sqrt' in str(equation),
    }
    
    # Check if target is already isolated (or nearly so)
    if (lhs == target and not target_in_rhs) or (rhs == target and not target_in_lhs):
        analysis['target_alone'] = True
    
    # Check if target is almost isolated (like 2*x or x/3)
    if not analysis['target_alone']:
        if target_in_lhs and not target_in_rhs:
            lhs_factors = lhs.as_ordered_factors() if hasattr(lhs, 'as_ordered_factors') else [lhs]
            if len(lhs_factors) == 2 and any(factor.is_number for factor in lhs_factors):
                analysis['target_almost_alone'] = True
                
        elif target_in_rhs and not target_in_lhs:
            rhs_factors = rhs.as_ordered_factors() if hasattr(rhs, 'as_ordered_factors') else [rhs]
            if len(rhs_factors) == 2 and any(factor.is_number for factor in rhs_factors):
                analysis['target_almost_alone'] = True
    
    return analysis

def get_hint(equation, target_var):
    """Generate a hint based on the current equation state"""
    analysis = analyze_equation_state(equation, target_var)
    target = sp.symbols(target_var)
    lhs, rhs = equation.args
    
    # Target on both sides
    if analysis['target_on_both_sides']:
        # Suggest getting the target to one side
        if target_var in str(lhs) and target_var in str(rhs):
            return f"Try to get all instances of {target_var} on one side. You could subtract {target_var} from both sides."
    
    # Target on one side but not isolated
    if analysis['target_on_left'] and not analysis['target_alone']:
        # Check if there's addition/subtraction
        if analysis['has_addition'] or analysis['has_subtraction']:
            return f"Try to isolate {target_var} by subtracting or adding terms to both sides."
        
        # Check if there's multiplication/division
        if analysis['has_multiplication']:
            return f"Try to isolate {target_var} by dividing both sides by the coefficient."
        
        if analysis['has_division']:
            return f"Try to isolate {target_var} by multiplying both sides to remove the division."
        
        # Check if there's a power
        if analysis['has_power'] and '**2' in str(lhs):
            return f"Try taking the square root of both sides to isolate {target_var}."
    
    # Target on right side but not isolated
    if analysis['target_on_right'] and not analysis['target_alone']:
        # First suggest moving to left side
        if not analysis['target_almost_alone']:
            return f"Consider moving {target_var} to the left side of the equation."
        
        # Otherwise, similar checks as above
        if analysis['has_addition'] or analysis['has_subtraction']:
            return f"Try to isolate {target_var} by subtracting or adding terms to both sides."
        
        if analysis['has_multiplication']:
            return f"Try to isolate {target_var} by dividing both sides by the coefficient."
        
        if analysis['has_division']:
            return f"Try to isolate {target_var} by multiplying both sides to remove the division."
        
        if analysis['has_power'] and '**2' in str(rhs):
            return f"Try taking the square root of both sides to isolate {target_var}."
    
    # Default hint
    return "Think about which operations would simplify the equation or help isolate the variable."

def apply_operation(equation, operation, value=None):
    """Apply an algebraic operation to both sides of the equation"""
    lhs, rhs = equation.args
    
    if operation == "add":
        if value is None:
            return equation
        return sp.Eq(lhs + value, rhs + value)
    
    elif operation == "subtract":
        if value is None:
            return equation
        return sp.Eq(lhs - value, rhs - value)
    
    elif operation == "multiply":
        if value is None or value == 0:
            return equation
        return sp.Eq(lhs * value, rhs * value)
    
    elif operation == "divide":
        if value is None or value == 0:
            return equation
        return sp.Eq(lhs / value, rhs / value)
    
    elif operation == "square":
        return sp.Eq(lhs ** 2, rhs ** 2)
    
    elif operation == "sqrt":
        try:
            return sp.Eq(sp.sqrt(lhs), sp.sqrt(rhs))
        except:
            return equation
    
    # If operation not recognized, return the original equation
    return equation

def minimal_simplify(equation):
    """Only perform basic simplification without solving"""
    try:
        # Just do basic expansion, NO SOLVING
        lhs = sp.expand(equation.lhs)
        rhs = sp.expand(equation.rhs)
        expanded = sp.Eq(lhs, rhs)
        
        # Only update if it actually simplifies without solving
        if count_operations(expanded) < count_operations(equation):
            return expanded
    except:
        pass
    
    return equation

def is_truly_solved(equation, target_var):
    """STRICT check if the target variable is truly isolated"""
    target = sp.symbols(target_var)
    lhs, rhs = equation.args
    
    # The target must be EXACTLY the symbol, not an expression containing it
    if (lhs == target and target not in rhs.free_symbols):
        return True
    
    if (rhs == target and target not in lhs.free_symbols):
        return True
    
    # Extra check - if it's x = number or number = x
    if (target in lhs.free_symbols and not target in rhs.free_symbols and 
        len(lhs.free_symbols) == 1 and len(rhs.free_symbols) == 0):
        return True
        
    if (target in rhs.free_symbols and not target in lhs.free_symbols and 
        len(rhs.free_symbols) == 1 and len(lhs.free_symbols) == 0):
        return True
    
    return False

def process_step(equation, operation, value, target_var):
    """Process a single algebraic step"""
    # Apply the operation
    new_eq = apply_operation(equation, operation, value)
    
    # Check if this makes any change
    if str(new_eq) == str(equation):
        return False, equation, "This operation doesn't change the equation."
    
    # Do minimal simplification
    simplified_eq = minimal_simplify(new_eq)
    
    # Check if solved
    solved = is_truly_solved(simplified_eq, target_var)
    
    # Generate feedback
    if solved:
        feedback = "¡Excelente! You've solved the equation correctly! 🎉"
    else:
        # Analyze if this was a good step
        old_analysis = analyze_equation_state(equation, target_var)
        new_analysis = analyze_equation_state(simplified_eq, target_var)
        
        if new_analysis['target_alone'] and not old_analysis['target_alone']:
            feedback = "¡Perfecto! That isolated the variable. Great work! 👏"
        elif old_analysis['target_on_both_sides'] and not new_analysis['target_on_both_sides']:
            feedback = "¡Bien hecho! You got the variable to one side of the equation."
        elif count_operations(simplified_eq) < count_operations(equation):
            feedback = "Good step! You simplified the equation. 👍"
        else:
            feedback = "That step changes the equation, but keeps the solution the same."
    
    return True, simplified_eq, feedback

def initialize_session_state():
    """Initialize all session state variables"""
    if 'problem' not in st.session_state:
        st.session_state.problem = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
    if 'solved' not in st.session_state:
        st.session_state.solved = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0
    if 'next_problem_data' not in st.session_state:
        st.session_state.next_problem_data = None
    if 'show_solution' not in st.session_state:
        st.session_state.show_solution = False
    if 'stars' not in st.session_state:
        st.session_state.stars = 0
    if 'hint_used' not in st.session_state:
        st.session_state.hint_used = False

def prepare_next_problem(difficulty):
    """Prepare the next problem in advance"""
    next_problem = generate_equation(difficulty)
    
    st.session_state.next_problem_data = {
        'problem': next_problem
    }

def switch_to_next_problem():
    """Switch to the next problem that was prepared in advance"""
    if st.session_state.next_problem_data:
        st.session_state.problem = st.session_state.next_problem_data['problem']
        st.session_state.feedback = ""
        st.session_state.solved = False
        st.session_state.show_solution = False
        st.session_state.question_id += 1
        st.session_state.next_problem_data = None
        st.session_state.hint_used = False
        return True
    return False

def main():
    st.title("Step-by-Step Algebra Practice")
    st.subheader("Solve for the variable one step at a time")
    
    initialize_session_state()
    
    # Sidebar for controls
    with st.sidebar:
        difficulty = st.selectbox(
            "Select difficulty:",
            ['easy', 'medium', 'hard', 'extra_hard']
        )
        
        # Prepare next problem when sidebar is rendered
        if st.session_state.next_problem_data is None:
            prepare_next_problem(difficulty)
            
        if st.button("New Problem"):
            # Add stars if the previous problem was solved
            if st.session_state.solved:
                # Bonus stars for not using hints
                hint_penalty = 1 if st.session_state.hint_used else 0
                
                if difficulty == 'easy':
                    st.session_state.stars += (2 - hint_penalty)
                elif difficulty == 'medium':
                    st.session_state.stars += (3 - hint_penalty)
                elif difficulty == 'hard':
                    st.session_state.stars += (4 - hint_penalty)
                else:  # extra_hard
                    st.session_state.stars += (6 - hint_penalty)
            
            if switch_to_next_problem():
                st.rerun()
            else:
                # Fallback if next problem wasn't prepared
                st.session_state.problem = generate_equation(difficulty)
                st.session_state.feedback = ""
                st.session_state.solved = False
                st.session_state.show_solution = False
                st.session_state.question_id += 1
                st.session_state.hint_used = False
        
        # Display stars
        st.subheader(f"Stars: ⭐ {st.session_state.stars}")
        
        # Show solution button (only available after several steps)
        if st.session_state.problem and len(st.session_state.problem['steps_taken']) >= 2:
            if st.button("Show Solution Path"):
                st.session_state.show_solution = True
                # Penalty for showing solution
                st.session_state.hint_used = True
    
    # Generate initial problem if needed
    if st.session_state.problem is None:
        st.session_state.problem = generate_equation(difficulty)
        st.session_state.question_id += 1
    
    # Display the current state of the problem
    st.markdown(f"### Solve for {st.session_state.problem['target_var']}")
    
    # Display equation with better formatting
    current_eq = st.session_state.problem['current_state']
    eq_latex = latex_equation(current_eq)
    st.latex(eq_latex)
    
    # Show steps taken so far
    if st.session_state.problem['steps_taken']:
        st.markdown("### Steps taken:")
        for i, step in enumerate(st.session_state.problem['steps_taken']):
            if 'display' in step:
                st.markdown(f"{i+1}. {step['display']}")
            elif 'operation' in step:
                if step['value'] is not None:
                    # Check if value is a symbolic expression
                    if hasattr(step['value'], 'name'):
                        st.markdown(f"{i+1}. {step['operation']} {step['value'].name}")
                    else:
                        st.markdown(f"{i+1}. {step['operation']} {step['value']}")
                else:
                    st.markdown(f"{i+1}. {step['operation']}")
    
    # If the problem is solved, show congratulations
    if st.session_state.solved:
        st.success(st.session_state.feedback)
        
        # Show how many stars were earned
        # Bonus stars for not using hints
        hint_penalty = 1 if st.session_state.hint_used else 0
        
        if difficulty == 'easy':
            stars_earned = 2 - hint_penalty
        elif difficulty == 'medium':
            stars_earned = 3 - hint_penalty
        elif difficulty == 'hard':
            stars_earned = 4 - hint_penalty
        else:  # extra_hard
            stars_earned = 6 - hint_penalty
        
        st.markdown(f"**You earned {stars_earned} ⭐!**")
        
        # Prepare next problem if needed
        if st.session_state.next_problem_data is None:
            prepare_next_problem(difficulty)
            
        if st.button("Try Another Problem", key="new_problem_button"):
            # Add stars
            if difficulty == 'easy':
                st.session_state.stars += (2 - hint_penalty)
            elif difficulty == 'medium':
                st.session_state.stars += (3 - hint_penalty)
            elif difficulty == 'hard':
                st.session_state.stars += (4 - hint_penalty)
            else:  # extra_hard
                st.session_state.stars += (6 - hint_penalty)
                
            if switch_to_next_problem():
                st.rerun()
            else:
                # Fallback
                st.session_state.problem = generate_equation(difficulty)
                st.session_state.feedback = ""
                st.session_state.solved = False
                st.session_state.show_solution = False
                st.session_state.question_id += 1
                st.session_state.hint_used = False
                st.rerun()
    else:
        # Show operation selection form
        st.markdown("### Choose an operation to apply:")
        
        # Create a form for operation selection
        col1, col2 = st.columns(2)
        
        with col1:
            operation = st.selectbox(
                "Operation:",
                ["add", "subtract", "multiply", "divide", "square", "sqrt"],
                key=f"operation_{st.session_state.question_id}"
            )
        
        with col2:
            # Only show value input for operations that need it
            if operation in ["add", "subtract", "multiply", "divide"]:
                value = st.number_input(
                    "Value:",
                    min_value=1, max_value=20, value=2,
                    key=f"value_{st.session_state.question_id}"
                )
            else:
                value = None
                st.write("No value needed for this operation")
        
        # Apply Operation button
        if st.button("Apply Operation", key=f"apply_{st.session_state.question_id}"):
            success, new_eq, feedback = process_step(
                st.session_state.problem['current_state'],
                operation,
                value,
                st.session_state.problem['target_var']
            )
            
            if success:
                # Update the equation
                st.session_state.problem['current_state'] = new_eq
                st.session_state.feedback = feedback
                
                # Add to steps taken
                step_display = f"{operation.capitalize()}"
                if value is not None:
                    step_display += f" {value}"
                
                st.session_state.problem['steps_taken'].append({
                    'operation': operation.capitalize(),
                    'value': value,
                    'display': step_display
                })
                
                # Check if solved
                if is_truly_solved(new_eq, st.session_state.problem['target_var']):
                    st.session_state.solved = True
                
                st.rerun()
            else:
                st.session_state.feedback = feedback
        
        # Hint button
        hint_col1, hint_col2 = st.columns([3, 1])
        with hint_col2:
            if st.button("Get Hint", key=f"hint_{st.session_state.question_id}"):
                hint = get_hint(st.session_state.problem['current_state'], st.session_state.problem['target_var'])
                st.session_state.feedback = f"💡 Hint: {hint}"
                st.session_state.hint_used = True
                st.rerun()
        
        # Display feedback
        if st.session_state.feedback:
            if "solved" in st.session_state.feedback.lower() or "excelente" in st.session_state.feedback.lower():
                st.success(st.session_state.feedback)
            elif "hint" in st.session_state.feedback.lower():
                st.info(st.session_state.feedback)
            elif "correcto" in st.session_state.feedback.lower() or "bien" in st.session_state.feedback.lower() or "good" in st.session_state.feedback.lower():
                st.info(st.session_state.feedback)
            else:
                st.warning(st.session_state.feedback)
    
    # Show solution path if requested
    if st.session_state.show_solution:
        st.markdown("### Solution Path:")
        st.markdown("Here's how to solve this equation:")
        
        target_var = st.session_state.problem['target_var']
        current_equation = st.session_state.problem['original_equation']
        
        steps = []
        for i, step in enumerate(st.session_state.problem['solution_steps']):
            operation = step['operation']
            value = step['value']
            
            # Format the step description
            if value is None:
                step_text = f"{i+1}. {operation}"
            else:
                step_text = f"{i+1}. {operation} {value}"
            
            # Apply the step
            if operation == "Take the square root":
                op = "sqrt"
            elif operation == "Square it":
                op = "square"
            elif operation == "Add":
                op = "add"
            elif operation == "Subtract":
                op = "subtract"
            elif operation == "Multiply by":
                op = "multiply"
            elif operation == "Divide by":
                op = "divide"
            else:
                op = operation.lower()
                
            current_equation = apply_operation(current_equation, op, value)
            current_equation = minimal_simplify(current_equation)
            
            # Add to solution steps
            steps.append({
                "text": step_text,
                "equation": latex_equation(current_equation)
            })
        
        # Display the solution steps
        for step in steps:
            st.markdown(step["text"])
            st.latex(step["equation"])
    
    # Show the original problem for reference
    with st.expander("Show original problem"):
        st.latex(latex_equation(st.session_state.problem['original_equation']))

if __name__ == "__main__":
    main()
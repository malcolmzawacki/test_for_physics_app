import streamlit as st
import random
import sympy as sp
from sympy import symbols, Eq, solve, sqrt, Pow, sympify
import re

def generate_equation(difficulty):
    """Generate a random algebra equation with a clear solution path"""
    variables = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
    
    # Define operations and their inverse operations
    operations = {
        'add': (lambda x, v: x + v, 'Subtract', lambda x, v: x - v),
        'sub': (lambda x, v: x - v, 'Add', lambda x, v: x + v),
        'mul': (lambda x, v: x * v, 'Divide by', lambda x, v: x / v),
        'div': (lambda x, v: x / v, 'Multiply by', lambda x, v: x * v),
        'exp': (lambda x, v: x ** v, 'Take the root', lambda x, v: x ** (1/v)),
        'root': (lambda x, v: x ** (1/v), 'Raise to power', lambda x, v: x ** v),
    }
    
    # Determine number of steps based on difficulty
    if difficulty == 'easy':
        num_steps = 2
    elif difficulty == 'medium':
        num_steps = 3
    elif difficulty == 'hard':
        num_steps = 4
    else:  # extra_hard
        num_steps = 5
    
    # Choose variables
    var_target = random.choice(variables)
    var_solve = random.choice([v for v in variables if v != var_target])
    
    # Generate the steps
    steps = []
    inverse_pairs = [
        {'add', 'sub'},
        {'mul', 'div'},
        {'exp', 'root'}
    ]
    
    prev_op = None
    for _ in range(num_steps):
        # Choose an operation that's not the inverse of the previous one
        op_name = random.choice(list(operations.keys()))
        is_inverse = False
        
        if prev_op:
            for pair in inverse_pairs:
                if prev_op in pair and op_name in pair and prev_op != op_name:
                    is_inverse = True
                    break
        
        # Keep choosing until we find a suitable operation
        while is_inverse or op_name == prev_op:
            op_name = random.choice(list(operations.keys()))
            is_inverse = False
            if prev_op:
                for pair in inverse_pairs:
                    if prev_op in pair and op_name in pair and prev_op != op_name:
                        is_inverse = True
                        break
        
        prev_op = op_name
        value = random.randint(2, 5)
        
        # Store the operation function, inverse name, and inverse function
        op_func, inverse_name, inverse_func = operations[op_name]
        steps.append((op_name, op_func, value, inverse_name, inverse_func))
    
    # Create the symbolic expressions
    target_sym = sp.symbols(var_target)
    solve_sym = sp.symbols(var_solve)
    
    # Build the equation from right to left (target = operations(solve))
    right_expr = target_sym
    for op_name, op_func, value, _, _ in steps:
        right_expr = op_func(right_expr, value)
    
    # Create the equation
    equation = sp.Eq(solve_sym, right_expr)
    
    # Create the solution steps (inverse operations in reverse order)
    solution_steps = []
    for op_name, _, value, inverse_name, inverse_func in reversed(steps):
        solution_steps.append({
            'name': inverse_name,
            'value': value,
            'func': inverse_func
        })
    
    return {
        'equation': equation,
        'target_var': var_target,
        'solve_var': var_solve,
        'solution_steps': solution_steps,
        'steps_taken': [],
        'current_state': equation,
        'original_equation': equation,
    }

def apply_operation(equation, operation, value, target_var):
    """Apply an operation to the equation to isolate the target variable"""
    # Parse the operation name to determine what to do
    op_map = {
        'Add': lambda x, v: x + v,
        'Subtract': lambda x, v: x - v,
        'Multiply by': lambda x, v: x * v,
        'Divide by': lambda x, v: x / v,
        'Take the root': lambda x, v: x ** (1/v),
        'Raise to power': lambda x, v: x ** v
    }
    
    # Get the function for this operation
    op_func = op_map.get(operation)
    if not op_func:
        return equation
    
    # Apply the operation to both sides of the equation
    lhs, rhs = equation.args
    target = sp.symbols(target_var)
    
    # Apply the appropriate transformation
    if target in rhs.free_symbols:
        # Target is on the right side, apply operation to both sides
        if operation in ['Multiply by', 'Divide by']:
            # Multiplication and division apply to both sides
            new_lhs = op_func(lhs, value)
            new_rhs = op_func(rhs, value)
        elif operation in ['Add', 'Subtract']:
            # Addition and subtraction apply to both sides
            new_lhs = op_func(lhs, value)
            new_rhs = op_func(rhs, value)
        else:
            # For powers and roots, we need to be more careful
            # Just transform the right side and check later if it's solved
            new_lhs = lhs
            new_rhs = op_func(rhs, value)
    else:
        # Target might be on the left or nested in complex expressions
        new_lhs = lhs
        new_rhs = op_func(rhs, value)
    
    # Return the new equation
    return sp.Eq(new_lhs, new_rhs)

def get_remaining_valid_operations(problem):
    """Determine what operations are valid at the current state of the equation"""
    current_eq = problem['current_state']
    target_var = problem['target_var']
    target = sp.symbols(target_var)
    
    # Check if target is already isolated
    if is_truly_solved(current_eq, target_var):
        return []  # Problem is solved
    
    # Get all remaining steps from original solution
    all_steps = problem['solution_steps']
    valid_ops = []
    taken_ops = problem['steps_taken']
    
    for step in all_steps:
        # Check if this step has already been taken
        already_taken = False
        for taken in taken_ops:
            if taken['name'] == step['name'] and taken['value'] == step['value']:
                already_taken = True
                break
                
        if not already_taken:
            # Apply this operation to see if it's helpful
            new_eq = apply_operation(current_eq, step['name'], step['value'], target_var)
            
            # Check if this operation makes progress (simplified check)
            # (The equations might differ in form but be mathematically equivalent)
            if new_eq != current_eq:
                valid_ops.append({'name': step['name'], 'value': step['value']})
    
    return valid_ops

def generate_options(valid_operations):
    """Generate 4 options for the user to choose from, including all valid operations"""
    # If there are no valid operations, return an empty list
    if not valid_operations:
        return []
    
    # All possible operations (for generating wrong answers)
    all_operations = [
        'Add', 'Subtract', 'Multiply by', 'Divide by', 
        'Take the root', 'Raise to power'
    ]
    
    # Create options from valid operations
    options = []
    for op in valid_operations:
        options.append(f"{op['name']} {op['value']}")
    
    # If we have fewer than 4 valid operations, add some wrong ones
    while len(options) < 4:
        wrong_op = random.choice(all_operations)
        wrong_value = random.randint(2, 5)
        wrong_option = f"{wrong_op} {wrong_value}"
        
        # Make sure it's not already in our options
        if wrong_option not in options:
            options.append(wrong_option)
    
    # Shuffle the options
    random.shuffle(options)
    return options

def latex_equation(equation):
    """Convert a sympy equation to a LaTeX string"""
    return sp.latex(equation)

def initialize_session_state():
    """Initialize the session state variables"""
    if 'problem' not in st.session_state:
        st.session_state.problem = None
    if 'options' not in st.session_state:
        st.session_state.options = []
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""
    if 'solved' not in st.session_state:
        st.session_state.solved = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0

def is_truly_solved(equation, target_var):
    """Check if the target variable is truly isolated (solved for)"""
    target = sp.symbols(target_var)
    lhs, rhs = equation.args
    
    # The target must be alone on one side
    if lhs == target:
        # And must not appear on the other side
        return target not in rhs.free_symbols
    
    # Special case: sometimes sympy puts the target on the right side
    if rhs == target:
        return target not in lhs.free_symbols
    
    return False

def process_step(option):
    """Process a step selection by the user"""
    # Parse the option
    parts = option.split()
    operation = " ".join(parts[:-1])
    value = int(parts[-1])
    
    # Check if this is a valid step
    valid_operations = get_remaining_valid_operations(st.session_state.problem)
    valid_op_strings = [f"{op['name']} {op['value']}" for op in valid_operations]
    
    if option in valid_op_strings:
        # Apply the operation to the current equation
        new_state = apply_operation(
            st.session_state.problem['current_state'],
            operation,
            value,
            st.session_state.problem['target_var']
        )
        
        # Record this step
        st.session_state.problem['steps_taken'].append({'name': operation, 'value': value})
        st.session_state.problem['current_state'] = new_state
        
        # Update feedback
        st.session_state.feedback = "¡Correcto! Good step."
        
        # Check if we've truly isolated the target variable
        if is_truly_solved(new_state, st.session_state.problem['target_var']):
            st.session_state.feedback = "🎉 Great job! You've solved the equation!"
            st.session_state.solved = True
        elif len(st.session_state.problem['steps_taken']) == len(st.session_state.problem['solution_steps']):
            # All steps completed but not solved - try to finalize
            try:
                target = sp.symbols(st.session_state.problem['target_var'])
                final_eq = sp.solve(new_state, target)
                if final_eq:
                    st.session_state.problem['current_state'] = sp.Eq(target, final_eq[0])
                    st.session_state.feedback = "🎉 Great job! You've solved the equation!"
                    st.session_state.solved = True
            except:
                pass
            
        # Generate new options
        valid_ops = get_remaining_valid_operations(st.session_state.problem)
        st.session_state.options = generate_options(valid_ops)
        
        return True
    else:
        st.session_state.feedback = "Try again. That's not a valid operation at this step."
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
        
        if st.button("New Problem"):
            st.session_state.problem = generate_equation(difficulty)
            st.session_state.options = generate_options(
                get_remaining_valid_operations(st.session_state.problem)
            )
            st.session_state.feedback = ""
            st.session_state.solved = False
            st.session_state.question_id += 1
    
    # Generate initial problem if needed
    if st.session_state.problem is None:
        st.session_state.problem = generate_equation(difficulty)
        valid_ops = get_remaining_valid_operations(st.session_state.problem)
        st.session_state.options = generate_options(valid_ops)
        st.session_state.question_id += 1
    
    # Display the current state of the problem
    st.markdown(f"### Solve for {st.session_state.problem['target_var']}")
    eq_latex = latex_equation(st.session_state.problem['current_state'])
    st.latex(eq_latex)
    
    # Show steps taken so far
    if st.session_state.problem['steps_taken']:
        st.markdown("### Steps taken:")
        for i, step in enumerate(st.session_state.problem['steps_taken']):
            st.markdown(f"{i+1}. {step['name']} {step['value']}")
    
    # If the problem is solved, show congratulations
    if st.session_state.solved:
        st.success(st.session_state.feedback)
        if st.button("Try Another Problem"):
            st.session_state.problem = generate_equation(difficulty)
            valid_ops = get_remaining_valid_operations(st.session_state.problem)
            st.session_state.options = generate_options(valid_ops)
            st.session_state.feedback = ""
            st.session_state.solved = False
            st.session_state.question_id += 1
    else:
        # Show options as buttons
        st.markdown("### What operation should you apply next?")
        
        # Create a container for the buttons
        button_container = st.container()
        
        # Create 2 rows of 2 buttons each
        if st.session_state.options:
            col1, col2 = button_container.columns(2)
            
            # First row
            if len(st.session_state.options) > 0:
                if col1.button(st.session_state.options[0], key=f"option_0_{st.session_state.question_id}"):
                    process_step(st.session_state.options[0])
                    st.rerun()
            
            if len(st.session_state.options) > 1:
                if col2.button(st.session_state.options[1], key=f"option_1_{st.session_state.question_id}"):
                    process_step(st.session_state.options[1])
                    st.rerun()
            
            # Second row
            col3, col4 = button_container.columns(2)
            
            if len(st.session_state.options) > 2:
                if col3.button(st.session_state.options[2], key=f"option_2_{st.session_state.question_id}"):
                    process_step(st.session_state.options[2])
                    st.rerun()
            
            if len(st.session_state.options) > 3:
                if col4.button(st.session_state.options[3], key=f"option_3_{st.session_state.question_id}"):
                    process_step(st.session_state.options[3])
                    st.rerun()
        
        # Display feedback
        if st.session_state.feedback:
            if "Correcto" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            elif "Great job" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
    
    # Show the original problem for reference
    with st.expander("Show original problem"):
        st.latex(latex_equation(st.session_state.problem['original_equation']))

if __name__ == "__main__":
    main()

"""definitely much better now! remaining issues are aesthetic, pretty much:
The buttons don't update if the path chosen is different than the one intended by the original encoding;
    if we have a = b/4  + 5, and choose to multiply by 4, it accepts it, and re-renders nicely as 4a = b + 20,
    but the next option is still "subtract 5", not "subtract 20" as it should be now
The more aesthetic issue is that the roots are not represented as decimal powers like (a+1)^0.25, rather than 4th root.
    For educational purposes, having the root is more reasonable, its what they're more used to seeing.
    I do like that the buttons handle powers and roots a little better now (take the root 4, raise to power 4)
    but it would still be better if it had a more natural sound "raise to the 4th power" "take the 4th root"
And this last one is silly, but I have to press "Try Another Problem" twice to get the equation to refresh.
    Oddly, the "show originial equation" part refreshes to a new problem on the first click, but the rest of the page doesn't
Ah, now I'm running into an additional oddness: when I "take the root 4" of something like (a-1)^4, it re-renders as ((a-1)^4)^0.25
    this is undesireable for obvious reasons lol
    Since the intended use of this page is just the order of operations and the movement of terms, maybe we can solve several of these
    problems at once by limiting the powers and roots to just 2. this wouldn't make a difference in terms of what is learned,
    but it would probably make the implementation a lot more smooth. and it would solve the awkward phrasing,
    since we can just hard-code 'take the square root' or 'square it'. doesn't solve everything, but a few things
"""
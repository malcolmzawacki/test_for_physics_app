import streamlit as st
import random

def generate_equation(difficulty):
    variables = ['x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
    operations = {
        'add': ('+', 'Subtract'),
        'sub': ('-', 'Add'),
        'mul': ('×', 'Divide by'),
        'div': ('÷', 'Multiply by'),
        'exp': ('^', 'Take the root'),
        'root': ('√', 'Square'),
    }

    if difficulty == 'easy':
        num_steps = 2
    elif difficulty == 'medium':
        num_steps = 3
    elif difficulty == 'hard':
        num_steps = 4
    elif difficulty == 'extra_hard':
        num_steps = 5

    var_target = random.choice(variables)
    var_solve = random.choice([v for v in variables if v != var_target])

    steps = []
    solution_steps = []
    prev_op = ''
    for _ in range(num_steps):
        op_name = random.choice(list(operations.keys()))
        while op_name == prev_op:
            op_name = random.choice(list(operations.keys()))
        prev_op = op_name

        value = random.randint(2, 5)

        symbol, inverse_text = operations[op_name]
        steps.append((op_name, symbol, value))
        solution_steps.append((inverse_text, value))

    right_side = var_target
    for op_name, symbol, value in steps:
        if op_name == 'mul':
            right_side = f"({right_side} · {value})"
        elif op_name == 'div':
            right_side = f"\\frac{{{right_side}}}{{{value}}}"
        elif op_name == 'add':
            right_side = f"({right_side} + {value})"
        elif op_name == 'sub':
            right_side = f"({right_side} - {value})"
        elif op_name == 'exp':
            right_side = f"({right_side} ^ {value})"
        elif op_name == 'root':
            right_side = f"\\sqrt[{value}]{{{right_side}}}"


    equation = f"{var_solve} = {right_side}"

    wrong_answers = []
    for _ in range(4):
      wrong = solution_steps.copy()
      change_idx = random.randrange(len(wrong))
      ops = list(operations.values())
      new_inverse = random.choice([op[1] for op in ops if op[1] != wrong[change_idx][0]])
      wrong[change_idx] = (new_inverse, wrong[change_idx][1])
      wrong_answers.append(wrong)

    all_answers = wrong_answers + [solution_steps]
    random.shuffle(all_answers)

    return {
        'equation': equation,
        'target_var': var_target,
        'solve_var': var_solve,
        'solution_steps': solution_steps,
        'choices': all_answers
    }

def initialize_session_state():
    if 'problem' not in st.session_state:
        st.session_state.problem = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0

def main():
    st.title("Algebraic Manipulation Practice")

    initialize_session_state()

    difficulty = st.selectbox(
        "Select difficulty:",
        ['easy', 'medium', 'hard', 'extra_hard']
    )

    if st.button("New Question") or st.session_state.problem is None:
        st.session_state.problem = generate_equation(difficulty)
        st.session_state.submitted = False
        st.session_state.question_id += 1

    if st.session_state.problem:
        st.latex(st.session_state.problem['equation'])

        choices = []
        for i, steps in enumerate(st.session_state.problem['choices']):
            steps_text = " → ".join([f"{step[0]} {step[1]}" for step in reversed(steps)])
            choices.append(f"Option {i+1}: {steps_text}")

        answer = st.radio(
            f"Select the correct sequence of steps to solve for {st.session_state.problem['target_var']}",
            options=choices,
            key=f"choice_{st.session_state.question_id}"
        )

        if st.button("Submit"):
            selected_index = int(answer[7]) - 1
            if st.session_state.problem['choices'][selected_index] == st.session_state.problem['solution_steps']:
                var_target = st.session_state.problem['target_var']
                var_solve = st.session_state.problem['solve_var']
                rearranged = f"{var_target} = "
                right_side = var_solve
                for step in reversed(st.session_state.problem['solution_steps']):
                    op = step[0].lower()
                    val = step[1]
                    if op.startswith('multiply'):
                        right_side = f"({right_side} · {val})"
                    elif op.startswith('divide'):
                        right_side = f"\\frac{{{right_side}}}{{{val}}}"
                    elif op.startswith('add'):
                        right_side = f"({right_side} + {val})"
                    elif op.startswith('subtract'):
                        right_side = f"({right_side} - {val})"
                    elif op.startswith('take the root'):
                        right_side = f"\\sqrt[{val}]{{{right_side}}}"
                    elif op.startswith('square'):
                        right_side = f"({right_side} ^ {val})"

                rearranged += right_side

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.latex(rearranged)
                with col2:
                    st.success("Correct!")
            else:
                st.error("Try again!")

if __name__ == "__main__":
    main()

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.linear_motion_generator import LinearMotionGenerator

def initialize_session_state():
    prefix = "linear_motion"
    base_vars = [
        'current_question',
        'correct_answer',
        'unit',
        'user_answer',
        'submitted',
        'question_id',
        'difficulty',
        'problem_type'
    ]
    
    # initialize all vars with prefix
    for var in base_vars:
        if f"{prefix}{var}" not in st.session_state:
            st.session_state[f"{prefix}{var}"] = None

    # initialize question_id to 0
    if f"{prefix}question_id" not in st.session_state:
        st.session_state[f"{prefix}question_id"] = 0


def generate_question(generator, problem_type, difficulty):
    prefix = "linear_motion"
    if problem_type == "No Time":
        question, answer, unit = generator.no_time_question(difficulty)
    elif problem_type == "No Distance":
        question, answer, unit = generator.no_dist_question(difficulty)
    elif problem_type == "No Acceleration":
        question, answer, unit = generator.no_acc_question(difficulty)
    elif problem_type == "No Final Velocity":
        question, answer, unit = generator.no_vf_question(difficulty)
    else:  # Mixed
        question, answer, unit = generator.mixed_question(difficulty)
    return question, answer, unit

    st.session_state.user_answer = None
    st.session_state.submitted = False
    #st.session_state[f"{prefix}question_id"] += 1

def main():
    st.title("Linear Motion Problems")
    prefix = "linear_motion"
    initialize_session_state()

    generator = LinearMotionGenerator()

    # UI Controls
    col1, col2 = st.columns(2)
    with col1:
        problem_types = {
        "Mixed": "Mixed",
        "No Time": r"v_f^2 = v_i^2 + 2a \cdot x",
        "No Distance": r"v_f = v_i + a \cdot t",
        "No Acceleration": r"x = \frac{(v_f + v_i)}{2} \cdot t",
        "No Final Velocity": r"x = v_i \cdot t + \frac{1}{2} a \cdot t^2",
        }


        selected_problem_type = st.selectbox(
            "Problem Type",
            options=list(problem_types.keys()),
            key="problem_type_select")
            
        if selected_problem_type != "Mixed":
            equation = problem_types[selected_problem_type]  # Exclude Mixed from standalone LaTeX rendering
            st.latex(equation)
        else:
            st.latex(r"v_f^2 = v_i^2 + 2a \cdot x")
            st.latex(r"x = v_i \cdot t + \frac{1}{2} a \cdot t^2")
        problem_type = selected_problem_type

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            key="difficulty_select"
        )
           
        if selected_problem_type == "Mixed":
            st.latex(r"v_f = v_i + a \cdot t")
            st.latex(r"x = \frac{(v_f + v_i)}{2} \cdot t")

    # Check if we need a new question
    if (problem_type != st.session_state[f"{prefix}problem_type"] or 
        st.session_state[f"{prefix}current_question"] is None):
        
        # Generate new question and store in session state
        question, answer, unit = generate_question(generator,problem_type, difficulty)
        st.session_state[f"{prefix}current_question"] = question
        st.session_state[f"{prefix}correct_answer"] = answer
        st.session_state[f"{prefix}unit"] = unit
        st.session_state[f"{prefix}problem_type"] = problem_type
        st.session_state[f"{prefix}question_id"] = 0
        generator.clear_answers()

    # Display current question
    st.write(st.session_state[f"{prefix}current_question"])
    
    # Input fields
    user_input = st.number_input(
        f"{st.session_state[f'{prefix}unit']}:",
        value=None,
        step=None,
        format="%f",
        key=f"{prefix}input_{st.session_state[f'{prefix}question_id']}"
    )

    # Submit button
    if st.button("Submit"):
        st.session_state[f"{prefix}submitted"] = True
        if user_input is not None:
            correct_answer = st.session_state[f"{prefix}correct_answer"]
            tolerance = correct_answer * 0.05
            
            if abs(user_input - correct_answer) < abs(tolerance):
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
        else:
            st.error("Please enter an answer before submitting.")
    
    # New Question button
    if st.button("New Question"):
        question, answer, unit = generate_question(generator, problem_type, difficulty)
        st.session_state[f"{prefix}question_id"] += 1
        st.session_state[f"{prefix}current_question"] = question
        st.session_state[f"{prefix}correct_answer"] = answer
        st.session_state[f"{prefix}unit"] = unit
        generator.clear_answers()
        st.rerun()

if __name__ == "__main__":
    main()

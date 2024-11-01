import streamlit as st

import random

st.set_page_config(page_title="Forces")
st.sidebar.header("Forces")

def generate_force_question():
    mass = random.randint(1, 10)  # kg
    acceleration = random.randint(1, 10)  # m/s²
    force = mass * acceleration
    question = f"If a mass of {mass:.2f} kg is accelerated at {acceleration:.2f} m/s², what is the force applied? (N)"
    return question, force

def generate_acceleration_question():
    force = random.randint(10, 100)  # N
    mass = random.randint(1, 10)  # kg
    acceleration = force / mass
    question = f"If a force of {force:.2f} N is applied to a mass of {mass:.2f} kg, what is the acceleration? (m/s²)"
    return question, acceleration

def initialize_session_state():
    if 'problem_type' not in st.session_state:
        st.session_state.problem_type = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0

def generate_new_question(problem_type):
    if problem_type == "Calculate Force":
        st.session_state.current_question, st.session_state.correct_answer = generate_force_question()
    elif problem_type == "Calculate Acceleration":
        st.session_state.current_question, st.session_state.correct_answer = generate_acceleration_question()
    st.session_state.problem_type = problem_type
    st.session_state.user_answer = None
    st.session_state.submitted = False
    st.session_state.question_id += 1  # Increment question ID for new input field key

def main():
    st.title("Forces Problems")

    initialize_session_state()

    problem_type = st.selectbox(
        "Select Problem Type",
        ("Calculate Force", "Calculate Acceleration"),
        key="problem_type_select"
    )

    if problem_type != st.session_state.problem_type:
        generate_new_question(problem_type)

    if st.session_state.current_question:
        st.write(st.session_state.current_question)
        
        unit = "N" if problem_type == "Calculate Force" else "m/s²"
        user_input = st.number_input(
            f"Your Answer ({unit}):",
            value=None,
            step=None,  # Remove step to allow any decimal input
            format="%f",  # Use %f to allow flexible decimal places
            key=f"user_input_{st.session_state.question_id}"  # Unique key for each question
        )

        if st.button("Submit"):
            st.session_state.submitted = True
            if user_input is not None:
                st.session_state.user_answer = user_input
                correct_answer = st.session_state.correct_answer
                tolerance = correct_answer * 0.05  # 5% tolerance

                if abs(st.session_state.user_answer - correct_answer) < tolerance:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
            else:
                st.error("Please enter an answer before submitting.")
        
        if st.button("New Question"):
            generate_new_question(problem_type)
            st.rerun()

    # Reset submitted flag if problem type changes
    if problem_type != st.session_state.problem_type:
        st.session_state.submitted = False

if __name__ == "__main__":
    main()
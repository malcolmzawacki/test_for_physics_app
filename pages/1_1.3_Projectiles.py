# pages/projectiles.py
import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.generators.projectile_generator import ProjectileGenerator

def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None
    if 'correct_answer2' not in st.session_state:
        st.session_state.correct_answer2 = None
    if 'unit' not in st.session_state:
        st.session_state.unit = None
    if 'unit2' not in st.session_state:
        st.session_state.unit2 = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'user_answer2' not in st.session_state:
        st.session_state.user_answer2 = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = None
    if 'problem_type' not in st.session_state:
        st.session_state.problem_type = None

def generate_new_question(generator, problem_type, difficulty):
    st.session_state.current_question, st.session_state.correct_answer, \
    st.session_state.correct_answer2, st.session_state.unit, st.session_state.unit2 = \
        generator.generate_question(problem_type, difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.problem_type = problem_type
    st.session_state.user_answer = None
    st.session_state.user_answer2 = None
    st.session_state.submitted = False
    st.session_state.question_id += 1

def main():
    st.title("Projectile Motion")
    
    initialize_session_state()
    
    # Create generator instance
    generator = ProjectileGenerator()
    
    # UI Controls
    col1, col2 = st.columns(2)
    with col1:
        problem_type = st.selectbox(
            "Select Problem Type",
            ["Type 1", "Type 2"],
            key="problem_type_select"
        )
    with col2:
        difficulty = st.selectbox(
            "Select Difficulty",
            ["Easy", "Hard"],
            key="difficulty_select"
        )

    # Generate new question if type or difficulty changes
    if (problem_type != st.session_state.problem_type or 
        difficulty != st.session_state.difficulty or 
        st.session_state.current_question is None):
        generate_new_question(generator, problem_type, difficulty)

    if st.session_state.current_question:
        st.write(st.session_state.current_question)
        
        # Input fields
        unit = st.session_state.unit
        user_input = st.number_input(
            f"{unit}:",
            value=None,
            step=None,
            format="%f",
            key=f"user_input_{st.session_state.question_id}"
        )
        
        # Second input for hard difficulty or type 2
        show_second_input = difficulty == "Hard" or (problem_type == "Type 2" and difficulty == "Easy")
        if show_second_input:
            unit2 = st.session_state.unit2
            user_input2 = st.number_input(
                f"{unit2}:",
                value=None,
                step=None,
                format="%f",
                key=f"user_input2_{st.session_state.question_id}"
            )

        # Submit button
        if st.button("Submit"):
            st.session_state.submitted = True
            if user_input is not None:
                st.session_state.user_answer = user_input
                correct_answer = st.session_state.correct_answer
                tolerance = abs(correct_answer * 0.05)
                
                if show_second_input:
                    if user_input2 is not None:
                        st.session_state.user_answer2 = user_input2
                        correct_answer2 = st.session_state.correct_answer2
                        tolerance2 = abs(correct_answer2 * 0.05)
                        
                        if (abs(user_input - correct_answer) < tolerance and 
                            abs(user_input2 - correct_answer2) < tolerance2):
                            st.success("Correct!")
                        else:
                            st.error(f"Incorrect. The correct answers are {correct_answer:.2f} {st.session_state.unit} "
                                   f"and {correct_answer2:.2f} {st.session_state.unit2}")
                    else:
                        st.error("Please enter both answers before submitting.")
                else:
                    if abs(user_input - correct_answer) < tolerance:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer:.2f} {st.session_state.unit}")
            else:
                st.error("Please enter an answer before submitting.")

        # New Question button
        if st.button("New Question"):
            generate_new_question(generator, problem_type, difficulty)
            st.rerun()

if __name__ == "__main__":
    main()
# pages/collisions.py
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.collision_generator import CollisionGenerator

def main():
    st.title("Collisions")
    
    # Create the generator
    generator = CollisionGenerator()
    generator.initialize_session_state()
    
    # UI Controls

    col1, col2 = st.columns(2)
    with col1:
        problem_type = st.selectbox(
            "Select Problem Type",
            ["Elastic Collision", "Inelastic Collision"],
            key="problem_type_select"
        )
    with col2:
        difficulty = st.selectbox(
            "Select Difficulty",
            ["Easy"],
            key="difficulty_select"
        )

    # Check if we need a new question
    prefix = generator.state_prefix
    if (problem_type != st.session_state[f"{prefix}problem_type"] or 
        st.session_state[f"{prefix}current_question"] is None):
        
        # Generate new question and store in session state
        question, answer, unit, answer2, unit2 = generator.generate_question(problem_type, difficulty)
        st.session_state[f"{prefix}current_question"] = question
        st.session_state[f"{prefix}correct_answer"] = answer
        st.session_state[f"{prefix}correct_answer2"] = answer2
        st.session_state[f"{prefix}unit"] = unit
        st.session_state[f"{prefix}unit2"] = unit2
        st.session_state[f"{prefix}problem_type"] = problem_type
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
            
            if abs(user_input - correct_answer) < tolerance:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
        else:
            st.error("Please enter an answer before submitting.")
    
    # New Question button
    if st.button("New Question"):
        st.session_state[f"{prefix}question_id"] += 1
        question, answer, unit, answer2, unit2 = generator.generate_question(problem_type, difficulty)
        st.session_state[f"{prefix}current_question"] = question
        st.session_state[f"{prefix}correct_answer"] = answer
        st.session_state[f"{prefix}correct_answer2"] = answer2
        st.session_state[f"{prefix}unit"] = unit
        st.session_state[f"{prefix}unit2"] = unit2
        generator.clear_answers()
        st.rerun()

if __name__ == "__main__":
    main()

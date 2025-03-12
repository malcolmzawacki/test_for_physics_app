import streamlit as st
import pandas as pd
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
        if f"{prefix}_{var}" not in st.session_state:
            st.session_state[f"{prefix}_{var}"] = None

    # initialize question_id to 0
    if f"{prefix}_question_id" not in st.session_state:
        st.session_state[f"{prefix}_question_id"] = 0
        
    # Initialize performance tracking dictionary if it doesn't exist
    if f"{prefix}_performance" not in st.session_state:
        # Structure: {problem_type: {difficulty: {'attempts': 0, 'correct': 0}}}
        problem_types = ["Mixed", "No Time", "No Distance", "No Acceleration", "No Final Velocity"]
        difficulties = ["Easy", "Medium", "Hard"]
        
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}
                
        st.session_state[f"{prefix}_performance"] = performance_dict


def generate_question(generator, problem_type, difficulty):
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


def update_performance(problem_type, difficulty, is_correct):
    """Update the performance tracking dictionary when an answer is submitted"""
    prefix = "linear_motion"
    performance = st.session_state[f"{prefix}_performance"]
    
    # Increment attempts
    performance[problem_type][difficulty]['attempts'] += 1
    
    # Increment correct if answer was correct
    if is_correct:
        performance[problem_type][difficulty]['correct'] += 1
    
    # Update session state
    st.session_state[f"{prefix}_performance"] = performance


def create_performance_dataframe():
    """Create a pandas DataFrame from the performance tracking dictionary"""
    prefix = "linear_motion"
    performance = st.session_state[f"{prefix}_performance"]
    
    # Create lists to hold data
    rows = []
    
    # Format data for dataframe
    for problem_type, difficulties in performance.items():
        for difficulty, stats in difficulties.items():
            attempts = stats['attempts']
            correct = stats['correct']
            
            # Calculate percentage or display NA if no attempts
            if attempts > 0:
                percentage = f"{(correct / attempts * 100):.1f}%"
                display = f"{correct}/{attempts} ({percentage})"
            else:
                display = "0/0 (0.0%)"
                
            rows.append({
                "Problem Type": problem_type,
                "Difficulty": difficulty,
                "Performance": display
            })
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Pivot the dataframe to get desired format
    pivot_df = df.pivot(index="Problem Type", columns="Difficulty", values="Performance")
    
    # Ensure all difficulty levels are present
    for col in ["Easy", "Medium", "Hard"]:
        if col not in pivot_df.columns:
            pivot_df[col] = "0/0 (0.0%)"
    
    # Reorder columns
    pivot_df = pivot_df[["Easy", "Medium", "Hard"]]
    
    return pivot_df


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
    if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
        st.session_state[f"{prefix}_current_question"] is None):
        
        # Generate new question and store in session state
        question, answer, unit = generate_question(generator, problem_type, difficulty)
        st.session_state[f"{prefix}_current_question"] = question
        st.session_state[f"{prefix}_correct_answer"] = answer
        st.session_state[f"{prefix}_unit"] = unit
        st.session_state[f"{prefix}_problem_type"] = problem_type
        st.session_state[f"{prefix}_submitted"] = False
        generator.clear_answers()

    # Display current question
    st.write(st.session_state[f"{prefix}_current_question"])
    
    # Input fields
    user_input = st.number_input(
        f"{st.session_state[f'{prefix}_unit']}:",
        value=None,
        step=None,
        format="%f",
        key=f"{prefix}_input_{st.session_state[f'{prefix}_question_id']}"
    )

    # Submit button
    if st.button("Submit"):
        if user_input is not None:
            correct_answer = st.session_state[f"{prefix}_correct_answer"]
            tolerance = correct_answer * 0.05
            is_correct = abs(user_input - correct_answer) < abs(tolerance)
            
            # Only update performance if not already submitted for this question
            if not st.session_state[f"{prefix}_submitted"]:
                update_performance(problem_type, difficulty, is_correct)
                st.session_state[f"{prefix}_submitted"] = True
            
            if is_correct:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
        else:
            st.error("Please enter an answer before submitting.")
    
    # New Question button
    if st.button("New Question"):
        st.session_state[f"{prefix}_question_id"] += 1
        question, answer, unit = generate_question(generator, problem_type, difficulty)
        st.session_state[f"{prefix}_current_question"] = question
        st.session_state[f"{prefix}_correct_answer"] = answer
        st.session_state[f"{prefix}_unit"] = unit
        st.session_state[f"{prefix}_submitted"] = False
        generator.clear_answers()
        st.rerun()
    
    # Display performance table
    st.subheader("Your Performance")
    performance_df = create_performance_dataframe()
    st.dataframe(performance_df, use_container_width=True)
    
    # Add a reset performance button
    if st.button("Reset Performance Statistics"):
        initialize_session_state()
        st.session_state[f"{prefix}_performance"] = {}
        st.rerun()

if __name__ == "__main__":
    main()
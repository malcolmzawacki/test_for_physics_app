import streamlit as st
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.generators._generator import Generator

"""Replaceables: default_class, default_prefix, default_tab, Default Title, generator (not search and replaceable)"""
"""Fillables: problem_type_dict, difficulties"""
class default_class:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "default": "default"
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy", "Medium", "Hard"]
        return problem_type_dict, problem_types, difficulties

    @staticmethod
    def clear_performance_dataframe():
        """Reset the performance tracking dictionary"""
        prefix = "default_prefix"
        _, problem_types, difficulties = default_class.question_parameters()
            
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict

    @staticmethod
    def initialize_session_state():
        prefix = "default_prefix"
        base_vars = [
        'current_question',
        'correct_answer',
        'unit',
        'user_answer',
        'submitted',
        '_question_id',
        'difficulty',
        'problem_type'
        ]

        # initialize question_id to 0
        if f"{prefix}_question_id" not in st.session_state:
            st.session_state[f"{prefix}_question_id"] = 0

        # initialize all vars with prefix
        for var in base_vars:
            if f"{prefix}_{var}" not in st.session_state:
                st.session_state[f"{prefix}_{var}"] = None if var != "_question_id" else 0
    
        # Initialize performance tracking dictionary if it doesn't exist
        if f"{prefix}_performance" not in st.session_state:
            st.session_state[f"{prefix}_performance"] = default_class.clear_performance_dataframe()
    
    @staticmethod
    def generate_question(generator, problem_type, difficulty):
        if problem_type == "":
            pass
        elif problem_type == "":
            pass
        else:
            pass
        return question, answer, unit

    @staticmethod
    def create_performance_dataframe():
        """Create a pandas DataFrame from the performance tracking dictionary"""
        prefix = "default_prefix"
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

    @staticmethod
    def update_performance(problem_type, difficulty, is_correct):
        """Update the performance tracking dictionary when an answer is submitted"""
        prefix = "default_prefix"
        performance = st.session_state[f"{prefix}_performance"]
        
        # Increment attempts
        performance[problem_type][difficulty]['attempts'] += 1
        
        # Increment correct if answer was correct
        if is_correct:
            performance[problem_type][difficulty]['correct'] += 1
        
        # Update session state
        st.session_state[f"{prefix}_performance"] = performance

    @staticmethod
    def default_tab():
        st.title("Default Title")
        prefix = "default_prefix"
        default_class.initialize_session_state()

        generator = _Generator()

        problem_type_dict, problem_types, difficulties = default_class.question_parameters()

        with st.expander("Your Performance", expanded=False):
            performance_df = default_class.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)

        # UI Controls
        col1, col2 = st.columns(2)
        with col1:

            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(problem_types),
                key="problem_type_select")
    
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                difficulties,
                key="difficulty_select"
            )
            
        # Check if we need a new question
        if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
            st.session_state[f"{prefix}_current_question"] is None):
            
            # Generate new question and store in session state
            question, answer, unit = default_class.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_problem_type"] = problem_type
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()

        # Display current question
        st.subheader("Question:")
        st.write(st.session_state[f"{prefix}_current_question"])

        # UI
        user_input = st.number_input(
                f"Answer (in {st.session_state[f'{prefix}_unit']}):",
                value=None,
                step=None,
                format="%f",
                key=f"{prefix}_input_{st.session_state[f'{prefix}_question_id']}"
            )
        
        # buttons
        in_col1, in_col2, in_col3 = st.columns(3)
        with in_col1:
            if st.button("Submit",key=f"{prefix}_submit"):
                if user_input is not None:
                    correct_answer = st.session_state[f"{prefix}_correct_answer"]
                    tolerance = correct_answer * 0.05
                    is_correct = abs(user_input - correct_answer) < abs(tolerance)
                    
                    # Only update performance if not already submitted for this question
                    if not st.session_state[f"{prefix}_submitted"]:
                        default_class.update_performance(problem_type, difficulty, is_correct)
                        st.session_state[f"{prefix}_submitted"] = True
                    
                    if is_correct:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
                else:
                    st.error("Please enter an answer before submitting.")
            
        with in_col2:
            st.write("")
           
        with in_col3:
            if st.button("New Question",key=f"{prefix}_new_question"):
                question, answer, unit = default_class.generate_question(generator, problem_type, difficulty)
                st.session_state[f"{prefix}_question_id"] += 1
                st.session_state[f"{prefix}_current_question"] = question
                st.session_state[f"{prefix}_correct_answer"] = answer
                st.session_state[f"{prefix}_unit"] = unit
                st.session_state[f"{prefix}_submitted"] = False
                generator.clear_answers()
                st.rerun()

        # Add a reset performance button further down
        st.write("")
        if st.button("Reset Performance Statistics",key=f"{prefix}_performance_reset"):
            default_class.initialize_session_state()
            st.session_state[f"{prefix}_performance"] = default_class.clear_performance_dataframe()
            question, answer, unit = default_class.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_question_id"] += 1
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            st.rerun()

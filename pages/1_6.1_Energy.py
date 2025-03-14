import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.energy_generator import EnergyGenerator
class energy_basics:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Elastic Potential Energy": r"EPE = \frac{1}{2} k \Delta x^2",
            "Kinetic Energy": r"KE = \frac{1}{2} m v^2",
            "Gravitational Potential Energy" : r"GPE = mgh",
            "Work": r"W = Fd",
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties
    
    @staticmethod
    def generate_question(generator, problem_type, difficulty):
        if problem_type == "Elastic Potential Energy":
            question, answer, unit = generator.elastic_problem(difficulty)
        elif problem_type == "Kinetic Energy":
            question, answer, unit = generator.kinetic_problem(difficulty)
        elif problem_type == "Gravitational Potential Energy":
            question, answer, unit = generator.gravitational_problem(difficulty)
        elif problem_type == "Work":
            question, answer, unit = generator.work_problem(difficulty)
        else:
            pass
        
        return question, answer, unit
    
    @staticmethod
    def clear_performance_dataframe():
        """Reset the performance tracking dictionary"""
        prefix = "energy_basics"
        _, problem_types, difficulties = energy_basics.question_parameters()
            
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict

    @staticmethod
    def initialize_session_state():
        prefix = "energy_basics"
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
            st.session_state[f"{prefix}_performance"] = energy_basics.clear_performance_dataframe()
    


    @staticmethod
    def create_performance_dataframe():
        """Create a pandas DataFrame from the performance tracking dictionary"""
        prefix = "energy_basics"
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
        for col in difficulties:
            if col not in pivot_df.columns:
                pivot_df[col] = "0/0 (0.0%)"
        
        # Reorder columns
        pivot_df = pivot_df[list(difficulties.keys())]
        
        return pivot_df

    @staticmethod
    def update_performance(problem_type, difficulty, is_correct):
        """Update the performance tracking dictionary when an answer is submitted"""
        prefix = "energy_basics"
        performance = st.session_state[f"{prefix}_performance"]
        
        # Increment attempts
        performance[problem_type][difficulty]['attempts'] += 1
        
        # Increment correct if answer was correct
        if is_correct:
            performance[problem_type][difficulty]['correct'] += 1
        
        # Update session state
        st.session_state[f"{prefix}_performance"] = performance

    @staticmethod
    def energy_basics_tab():
        st.title("Types of Energy Problems")
        prefix = "energy_basics"
        energy_basics.initialize_session_state()

        generator = EnergyGenerator()

        problem_type_dict, problem_types, difficulties = energy_basics.question_parameters()
        with st.expander("Your Performance", expanded=False):
            performance_df = energy_basics.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)

        # UI Controls
        col1, col2 = st.columns(2)
        with col1:

            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(problem_types),
                key=f"{prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                difficulties,
                key=f"{prefix}_difficulty_select"
            )
       
        # Check if we need a new question
        if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
            st.session_state[f"{prefix}_current_question"] is None):
            
            # Generate new question and store in session state
            question, answer, unit = energy_basics.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_problem_type"] = problem_type
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()

        # Display current question
        st.subheader("Question:")
        st.write(st.session_state[f"{prefix}_current_question"])
        
        # Input fields
        user_input = st.number_input(
                f"Answer (in {st.session_state[f'{prefix}_unit']}):",
                value=None,
                step=None,
                format="%f",
                key=f"{prefix}_input_{st.session_state[f'{prefix}_question_id']}"
            )
        
        in_col1, in_col2, in_col3 = st.columns(3)

        with in_col1: # submit button
            if st.button("Submit",key=f"{prefix}_submit"):
                if user_input is not None:
                    correct_answer = st.session_state[f"{prefix}_correct_answer"]
                    tolerance = correct_answer * 0.05
                    is_correct = abs(user_input - correct_answer) < abs(tolerance)
                    
                    # Only update performance if not already submitted for this question
                    if not st.session_state[f"{prefix}_submitted"]:
                        energy_basics.update_performance(problem_type, difficulty, is_correct)
                        st.session_state[f"{prefix}_submitted"] = True
                    
                    if is_correct:
                        st.success("Correct!")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
                else:
                    st.error("Please enter an answer before submitting.")
        with in_col2: # spacing
            st.write("")            
           
        with in_col3: #new question button
            if st.button("New Question",key=f"{prefix}_new_question"):
                question, answer, unit = energy_basics.generate_question(generator, problem_type, difficulty)
                st.session_state[f"{prefix}_question_id"] += 1
                st.session_state[f"{prefix}_current_question"] = question
                st.session_state[f"{prefix}_correct_answer"] = answer
                st.session_state[f"{prefix}_unit"] = unit
                st.session_state[f"{prefix}_submitted"] = False
                generator.clear_answers()
                st.rerun()

        # reset performance button

        if st.button("Reset Performance Statistics",key=f"{prefix}_performance_reset"):
            energy_basics.initialize_session_state()
            st.session_state[f"{prefix}_performance"] = energy_basics.clear_performance_dataframe()
            question, answer, unit = energy_basics.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_question_id"] += 1
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            st.rerun()


class energy_conservation:

    @staticmethod
    def question_parameters():
        """Holds current options for questions for centralized updating"""
        problem_type_dict = {
            "Elastic <--> Kinetic": r"\frac{1}{2} m v^2 = \frac{1}{2} k \Delta x^2",
            "Gravitational <--> Kinetic": r"mgh = \frac{1}{2} m v^2",
            "Gravitational <--> Elastic" : r"mgh = \frac{1}{2} k \Delta x^2",
            }
        problem_types = list(problem_type_dict.keys())
        difficulties = ["Easy","Medium","Hard"]
        return problem_type_dict, problem_types, difficulties
    
    @staticmethod
    def generate_question(generator, problem_type, difficulty):
        if problem_type == "Elastic <--> Kinetic":
            question, answer, unit = generator.elastic_kinetic_problem(difficulty)
        elif problem_type == "Gravitational <--> Kinetic":
            question, answer, unit = generator.kinetic_gravitational_problem(difficulty)
        elif problem_type == "Gravitational <--> Elastic":
            question, answer, unit = generator.elastic_gravitational_problem(difficulty)
        else:
            pass
        
        return question, answer, unit
    
    @staticmethod
    def clear_performance_dataframe():
        """Reset the performance tracking dictionary"""
        prefix = "energy_conservation"
        _, problem_types, difficulties = energy_conservation.question_parameters()
            
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict

    @staticmethod
    def initialize_session_state():
        prefix = "energy_conservation"
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
            st.session_state[f"{prefix}_performance"] = energy_conservation.clear_performance_dataframe()
    


    @staticmethod
    def create_performance_dataframe():
        """Create a pandas DataFrame from the performance tracking dictionary"""
        prefix = "energy_conservation"
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
        for col in difficulties:
            if col not in pivot_df.columns:
                pivot_df[col] = "0/0 (0.0%)"
        
        # Reorder columns
        pivot_df = pivot_df[list(difficulties.keys())]
        
        return pivot_df

    @staticmethod
    def update_performance(problem_type, difficulty, is_correct):
        """Update the performance tracking dictionary when an answer is submitted"""
        prefix = "energy_conservation"
        performance = st.session_state[f"{prefix}_performance"]
        
        # Increment attempts
        performance[problem_type][difficulty]['attempts'] += 1
        
        # Increment correct if answer was correct
        if is_correct:
            performance[problem_type][difficulty]['correct'] += 1
        
        # Update session state
        st.session_state[f"{prefix}_performance"] = performance

    @staticmethod
    def energy_conservation_tab():
        st.title("Conservation of Energy Problems")
        prefix = "energy_conservation"
        energy_conservation.initialize_session_state()

        generator = EnergyGenerator()

        problem_type_dict, problem_types, difficulties = energy_conservation.question_parameters()

        with st.expander("Your Performance", expanded=False):
            performance_df = energy_conservation.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)
        # UI Controls
        col1, col2 = st.columns(2)
        with col1:

            selected_problem_type = st.selectbox(
                "Problem Type",
                options=list(problem_types),
                key=f"{prefix}_problem_type_select")
                
            problem_type = selected_problem_type

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                difficulties,
                key=f"{prefix}_difficulty_select"
            )

           
        # Check if we need a new question
        if (problem_type != st.session_state[f"{prefix}_problem_type"] or 
            st.session_state[f"{prefix}_current_question"] is None):
            
            # Generate new question and store in session state
            question, answer, unit = energy_conservation.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_problem_type"] = problem_type
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()

        # Display current question
        st.subheader("Question:")
        st.write(st.session_state[f"{prefix}_current_question"])
        user_input = st.number_input(
                f"Answer (in {st.session_state[f'{prefix}_unit']}):",
                value=None,
                step=None,
                format="%f",
                key=f"{prefix}_input_{st.session_state[f'{prefix}_question_id']}"
            )
        in_col1, in_col2, in_col3 = st.columns(3)
        # Input fields
        with in_col1:
            if st.button("Submit",key=f"{prefix}_submit"):
                if user_input is not None:
                    correct_answer = st.session_state[f"{prefix}_correct_answer"]
                    tolerance = correct_answer * 0.05
                    is_correct = abs(user_input - correct_answer) < abs(tolerance)
                    
                    # Only update performance if not already submitted for this question
                    if not st.session_state[f"{prefix}_submitted"]:
                        energy_conservation.update_performance(problem_type, difficulty, is_correct)
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
                question, answer, unit = energy_conservation.generate_question(generator, problem_type, difficulty)
                st.session_state[f"{prefix}_question_id"] += 1
                st.session_state[f"{prefix}_current_question"] = question
                st.session_state[f"{prefix}_correct_answer"] = answer
                st.session_state[f"{prefix}_unit"] = unit
                st.session_state[f"{prefix}_submitted"] = False
                generator.clear_answers()
                st.rerun()
            st.write("")
             # Submit button
            
            # New Question button
            
        

        
        # Add a reset performance button

        if st.button("Reset Performance Statistics",key=f"{prefix}_performance_reset"):
            energy_conservation.initialize_session_state()
            st.session_state[f"{prefix}_performance"] = energy_conservation.clear_performance_dataframe()
            question, answer, unit = energy_conservation.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_question_id"] += 1
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            st.rerun()


def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2 = st.tabs(["Types of Energy", "Conservation of Energy"])
    
    
    with tab1:
        energy_basics.energy_basics_tab()
    with tab2:
        energy_conservation.energy_conservation_tab()

if __name__ == "__main__":
    main()
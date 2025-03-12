import streamlit as st
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")

sys.path.append(str(Path(__file__).parent.parent))
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.generators.projectile_generator import ProjectileGenerator

def generate_position_time_graph():
    """
    Returns (fig, direction, motion_state, graph_label) for a randomly generated position-time graph
    """
    fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
    t = np.linspace(0, 5, 100)

    # Randomly pick one of four "types"
    graph_type = random.choice(["linear_positive", "linear_negative", 
                                "acceleration_positive", "acceleration_negative"])

    if graph_type == "linear_positive":
        position = 2 * t + 1    # slope > 0, constant velocity
        correct_direction = "Forward"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "linear_negative":
        position = -1.5 * t + 5 # slope < 0, constant velocity
        correct_direction = "Backward"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "acceleration_positive":
        position = t**2         # slope increasing over time
        correct_direction = "Forward"
        correct_motion_state = "Accelerating (positive)"
    else:  # "acceleration_negative"
        position = -0.5 * t**2 + 5
        correct_direction = "Backward"
        correct_motion_state = "Accelerating (negative)"

    ax.plot(t, position, color="cyan")
    ax.set_xlabel("Time (s)", color="white")
    ax.set_ylabel("Position (m)", color="white")
    ax.set_title("Position-Time Graph", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.tight_layout()

    return (fig, correct_direction, correct_motion_state)

def generate_velocity_time_graph():
    """
    Returns (fig, direction, motion_state) for a randomly generated velocity-time graph
    """
    fig, ax = plt.subplots(figsize=(3, 2))  # Smaller figure size
    t = np.linspace(0, 5, 100)

    # Randomly pick one of four "types"
    graph_type = random.choice(["constant_positive", "constant_negative", 
                                "increasing_positive", "decreasing_negative"])

    if graph_type == "constant_positive":
        velocity = np.ones_like(t) * 2  # constant velocity > 0
        correct_direction = "Forward"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "constant_negative":
        velocity = np.ones_like(t) * -1.5  # constant velocity < 0
        correct_direction = "Backward"
        correct_motion_state = "Constant Velocity"
    elif graph_type == "increasing_positive":
        velocity = t  # starts at 0, increasing
        correct_direction = "Forward"
        correct_motion_state = "Accelerating (positive)"
    else:  # "decreasing_negative"
        velocity = -0.5 * t - 1  # negative velocity, becomes more negative
        correct_direction = "Backward"
        correct_motion_state = "Accelerating (negative)"

    ax.plot(t, velocity, color="orange")
    ax.set_xlabel("Time (s)", color="white")
    ax.set_ylabel("Velocity (m/s)", color="white")
    ax.set_title("Velocity-Time Graph", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.tight_layout()

    return (fig, correct_direction, correct_motion_state)

def graphing_practice():
    st.title("Position-Time and Velocity-Time Graph Recognition")
    st.write("Use this page to practice identifying direction and state of motion from different graphs.")

    # Use session state to store the current graph (so it doesn't regenerate on button press)
    if "pt_graph" not in st.session_state:
        st.session_state.pt_graph = None
    if "vt_graph" not in st.session_state:
        st.session_state.vt_graph = None

    # For matching mode, we'll store multiple graphs
    if "match_pt_graph" not in st.session_state:
        st.session_state.match_pt_graph = None
    if "match_vt_graph" not in st.session_state:
        st.session_state.match_vt_graph = None
    if "option_graphs" not in st.session_state:
        st.session_state.option_graphs = None

    mode = st.selectbox("Select a Practice Mode:", 
                    ["Position-Time Graph", "Velocity-Time Graph", "Match Graphs"])

    # --------------------------------------------
    # 1) POSITION-TIME GRAPH
    # --------------------------------------------
    if mode == "Position-Time Graph":
        # If there's no stored graph yet or user wants a new one, generate it
        if st.button("Generate New Graph"):
            st.session_state.pt_graph = generate_position_time_graph()

        # If we have a stored graph, display it
        if st.session_state.pt_graph is not None:
            fig, correct_dir, correct_state = st.session_state.pt_graph
            probCol1, probCol2 = st.columns(2)
            with probCol1:
                st.pyplot(fig)
            with probCol2:
                # Let user pick answers
                user_dir = st.selectbox(
                    "Select the direction of motion:", 
                    ["Forward", "Backward"]
                )
                user_state = st.selectbox(
                    "Select the state of motion:", 
                    ["Constant Velocity", "Accelerating (positive)", "Accelerating (negative)"]
                )

            if st.button("Check Answers"):
                # Compare to correct answers
                direction_correct = (user_dir == correct_dir)
                state_correct = (user_state == correct_state)

                if direction_correct and state_correct:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct direction is '{correct_dir}' and the motion state is '{correct_state}'.")
        else:
            st.info("Click 'Generate New Graph' to start.")

    # --------------------------------------------
    # 2) VELOCITY-TIME GRAPH
    # --------------------------------------------
    elif mode == "Velocity-Time Graph":
        # If there's no stored graph yet or user wants a new one, generate it
        if st.button("Generate New Graph"):
            st.session_state.vt_graph = generate_velocity_time_graph()

        # If we have a stored graph, display it
        if st.session_state.vt_graph is not None:
            fig, correct_dir, correct_state = st.session_state.vt_graph
            probCol1, probCol2 = st.columns(2)
            with probCol1:
                st.pyplot(fig)
            with probCol2:
                # Let user pick answers
                user_dir = st.selectbox(
                    "Select the direction of motion:", 
                    ["Forward", "Backward"]
                )
                user_state = st.selectbox(
                    "Select the state of motion:", 
                    ["Constant Velocity", "Accelerating (positive)", "Accelerating (negative)"]
                )

            if st.button("Check Answers"):
                direction_correct = (user_dir == correct_dir)
                state_correct = (user_state == correct_state)

                if direction_correct and state_correct:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct direction is '{correct_dir}' and the motion state is '{correct_state}'.")
        else:
            st.info("Click 'Generate New Graph' to start.")

    # --------------------------------------------
    # 3) MATCH GRAPHS
    # --------------------------------------------
    else:
        st.write("You'll see either a position-time or velocity-time graph and try to match it among multiple options of the other type.")

        # We randomly decide which main graph to show (P-T or V-T)
        show_pt_first = st.selectbox("Which primary graph type?", 
                                 ["Position-Time First", "Velocity-Time First"])

        if show_pt_first == "Position-Time First":
            # If we don't have a stored graph or user wants a new scenario
            if st.button("Generate New Matching Set"):
                st.session_state.match_pt_graph = generate_position_time_graph()
                # Generate 3 velocity-time option graphs
                st.session_state.option_graphs = [
                    generate_velocity_time_graph() for _ in range(3)
                ]

            if st.session_state.match_pt_graph is not None:
                fig_pt, dir_pt, state_pt = st.session_state.match_pt_graph
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    st.pyplot(fig_pt)
                    st.write("Match this Position-Time Graph to the correct Velocity-Time Graph")

                # Display option graphs in columns
                if st.session_state.option_graphs:
                    option_columns = col2,col3,col4
                    labels = ["A", "B", "C"]

                    for col, label, (fig_vt, dir_vt, state_vt) in zip(option_columns, labels, st.session_state.option_graphs):
                        with col:
                            st.pyplot(fig_vt)
                            st.write(f"Option {label}")
                            

                    # Let user pick which one is correct
                    user_choice = st.selectbox(
                        "Which Velocity-Time graph matches the Positon-Time graph above?", 
                        labels
                    )

                    if st.button("Check Match"):
                        chosen_index = labels.index(user_choice)
                        _, dir_vt_selected, state_vt_selected = st.session_state.option_graphs[chosen_index]

                        # Basic matching logic: compare direction & motion state
                        # (You might want more sophisticated logic in practice)
                        if (dir_pt == dir_vt_selected) and (state_pt == state_vt_selected):
                            st.success("Correct match!")
                        else:
                            st.error("Incorrect match. Try again or generate a new set.")
                else:
                    st.info("Click 'Generate New Matching Set' to see the option graphs.")

        else:  # Velocity-Time First
            if st.button("Generate New Matching Set"):
                st.session_state.match_vt_graph = generate_velocity_time_graph()
                # Generate 3 position-time option graphs
                st.session_state.option_graphs = [
                    generate_position_time_graph() for _ in range(3)
                ]

            if st.session_state.match_vt_graph is not None:
                fig_vt, dir_vt, state_vt = st.session_state.match_vt_graph
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    st.pyplot(fig_vt)
                    st.write("Match this Velocity-Time Graph to the correct Position-Time Graph below.")

                if st.session_state.option_graphs:
                    option_columns = col2,col3,col4
                    labels = ["A", "B", "C"]

                    for col, label, (fig_pt, dir_pt, state_pt) in zip(option_columns, labels, st.session_state.option_graphs):
                        with col:
                            st.pyplot(fig_pt)
                            st.write(f"Option {label}")

                    user_choice = st.selectbox(
                        "Which Position-Time graph matches the V-T graph above?",
                        labels
                    )

                    if st.button("Check Match"):
                        chosen_index = labels.index(user_choice)
                        _, dir_pt_selected, state_pt_selected = st.session_state.option_graphs[chosen_index]

                        if (dir_pt_selected == dir_vt) and (state_pt_selected == state_vt):
                            st.success("Correct match!")
                        else:
                            st.error("Incorrect match. Try again or generate a new set.")
                else:
                    st.info("Click 'Generate New Matching Set' to see the option graphs.")


class linear_fns:

    @staticmethod
    def clear_performance_dataframe():
        """Reset the performance tracking dictionary"""
        prefix = "linear_motion"
        problem_types = ["Mixed", "No Time", "No Distance", "No Acceleration", "No Final Velocity"]
        difficulties = ["Easy", "Medium", "Hard"]
            
        performance_dict = {}
        for p_type in problem_types:
            performance_dict[p_type] = {}
            for diff in difficulties:
                performance_dict[p_type][diff] = {'attempts': 0, 'correct': 0}     
        st.session_state[f"{prefix}_performance"] = performance_dict
        return performance_dict

    @staticmethod
    def initialize_session_state():
        prefix = "linear_motion"
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
            st.session_state[f"{prefix}_performance"] = linear_fns.clear_performance_dataframe()
    
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def linear_motion_problems():
        st.title("Linear Motion Problems")
        prefix = "linear_motion"
        linear_fns.initialize_session_state()

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
            question, answer, unit = linear_fns.generate_question(generator, problem_type, difficulty)
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
        if st.button("Submit",key=f"{prefix}_submit"):
            if user_input is not None:
                correct_answer = st.session_state[f"{prefix}_correct_answer"]
                tolerance = correct_answer * 0.05
                is_correct = abs(user_input - correct_answer) < abs(tolerance)
                
                # Only update performance if not already submitted for this question
                if not st.session_state[f"{prefix}_submitted"]:
                    linear_fns.update_performance(problem_type, difficulty, is_correct)
                    st.session_state[f"{prefix}_submitted"] = True
                
                if is_correct:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is {correct_answer:.2f}.")
            else:
                st.error("Please enter an answer before submitting.")
        
        # New Question button
        if st.button("New Question",key=f"{prefix}_new_question"):
            question, answer, unit = linear_fns.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_question_id"] += 1
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            st.rerun()
        
        with st.expander("Your Performance", expanded=False):
            performance_df = linear_fns.create_performance_dataframe()
            st.dataframe(performance_df, use_container_width=True)
        
        # Add a reset performance button
        if st.button("Reset Performance Statistics",key=f"{prefix}_performance_reset"):
            linear_fns.initialize_session_state()
            st.session_state[f"{prefix}_performance"] = linear_fns.clear_performance_dataframe()
            question, answer, unit = linear_fns.generate_question(generator, problem_type, difficulty)
            st.session_state[f"{prefix}_question_id"] += 1
            st.session_state[f"{prefix}_current_question"] = question
            st.session_state[f"{prefix}_correct_answer"] = answer
            st.session_state[f"{prefix}_unit"] = unit
            st.session_state[f"{prefix}_submitted"] = False
            generator.clear_answers()
            st.rerun()



class Projectile_fns:
    @staticmethod
    def initialize_projectile_session_state():
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
    @staticmethod
    def generate_new_projectile_question(generator, problem_type, difficulty):
        st.session_state.current_question, st.session_state.correct_answer, \
        st.session_state.correct_answer2, st.session_state.unit, st.session_state.unit2 = \
            generator.generate_question(problem_type, difficulty)
        st.session_state.difficulty = difficulty
        st.session_state.problem_type = problem_type
        st.session_state.user_answer = None
        st.session_state.user_answer2 = None
        st.session_state.submitted = False
        st.session_state.question_id += 1
    
    @staticmethod
    def projectile_practice():
        st.title("Projectile Motion")
        
        Projectile_fns.initialize_projectile_session_state()
        
        # Create generator instance
        generator = ProjectileGenerator()
        
        # UI Controls
        col1, col2 = st.columns(2)
        with col1:
            proj_problem_type = st.selectbox(
                "Select Problem Type",
                ["Type 1", "Type 2","Type 3"],
                key="proj_problem_type_select"
            )
        with col2:
            difficulty = st.selectbox(
                "Select Difficulty",
                ["Easy", "Hard"],
                key="proj_difficulty_select"
            )

        # Generate new question if type or difficulty changes
        if (proj_problem_type != st.session_state.problem_type or 
            difficulty != st.session_state.difficulty or 
            st.session_state.current_question is None):
            Projectile_fns.generate_new_projectile_question(generator, proj_problem_type, difficulty)

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
            show_second_input = difficulty == "Hard" or ((proj_problem_type == "Type 2" or proj_problem_type == "Type 3") and difficulty == "Easy")
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
            if st.button("Submit", key = "proj_submit_button"):
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
                Projectile_fns.generate_new_projectile_question(generator, proj_problem_type, difficulty)
                st.rerun()


def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2,tab3 = st.tabs(["Linear Motion Problems", "Graphing Practice","Projectile Practice"])
    
    
    with tab1:
        linear_fns.linear_motion_problems()
    
    with tab2:
        graphing_practice()
    with tab3:
        Projectile_fns.projectile_practice()

if __name__ == "__main__":
    main()

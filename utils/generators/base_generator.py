
import streamlit as st

class BaseGenerator:
    def __init__(self, state_prefix):
        self.state_prefix = state_prefix
    
    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 10
        elif difficulty == "Hard":
            return 50
        else:
            return 20
    
    def initialize_session_state(self):
        """Initialize basic session state variables with proper prefixing"""
        vars_to_init = [
            'current_question',
            'correct_answer',
            'correct_answer2',
            'unit',
            'unit2',
            'user_answer',
            'user_answer2',
            'submitted',
            'question_id',
            'difficulty',
            'problem_type'
        ]
        
        for var in vars_to_init:
            key = f"{self.state_prefix}{var}"
            if key not in st.session_state:
                if not key == 'question_id':
                    st.session_state[key] = None
                else:
                    st.session_state[key] = 0
    
    def clear_answers(self):
        """Clear user answers when generating new questions"""
        st.session_state[f"{self.state_prefix}user_answer"] = None
        st.session_state[f"{self.state_prefix}user_answer2"] = None
        st.session_state[f"{self.state_prefix}submitted"] = False


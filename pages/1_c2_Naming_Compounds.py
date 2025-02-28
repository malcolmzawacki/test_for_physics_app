import streamlit as st
import math
import random


element_dict = {
    #"Period 1"
    'H': {'name': 'Hydrogen', 'period': 1, 'group': 1, 'charges': [1], 'anion': 'hydride'},
    
    #"Period 2"
    'Li': {'name': 'Lithium', 'period': 2, 'group': 1, 'charges': [1], 'anion': None},
    'Be': {'name': 'Beryllium', 'period': 2, 'group': 2, 'charges': [2], 'anion': None},
    'B': {'name': 'Boron', 'period': 2, 'group': 13, 'charges': [-3], 'anion': 'boride'},
    'C': {'name': 'Carbon', 'period': 2, 'group': 14, 'charges': [-4], 'anion': 'carbide'},
    'N': {'name': 'Nitrogen', 'period': 2, 'group': 15, 'charges': [-3], 'anion': 'nitride'},
    'O': {'name': 'Oxygen', 'period': 2, 'group': 16, 'charges': [-2], 'anion': 'oxide'},
    'F': {'name': 'Fluorine', 'period': 2, 'group': 17, 'charges': [-1], 'anion': 'fluoride'},

    #"Period 3"
    'Na': {'name': 'Sodium', 'period': 3, 'group': 1, 'charges': [1], 'anion': None},
    'Mg': {'name': 'Magnesium', 'period': 3, 'group': 2, 'charges': [2], 'anion': None},
    'Al': {'name': 'Aluminum', 'period': 3, 'group': 13, 'charges': [3], 'anion': 'aluminide'},
    'Si': {'name': 'Silicon', 'period': 3, 'group': 14, 'charges': [-4], 'anion': 'silicide'},
    'P': {'name': 'Phosphorus', 'period': 3, 'group': 15, 'charges': [-3], 'anion': 'phosphide'},
    'S': {'name': 'Sulfur', 'period': 3, 'group': 16, 'charges': [-2], 'anion': 'sulfide'},
    'Cl': {'name': 'Chlorine', 'period': 3, 'group': 17, 'charges': [-1], 'anion': 'chloride'},

    #"Period 4"
    'K': {'name': 'Potassium', 'period': 4, 'group': 1, 'charges': [1], 'anion': None},
    'Ca': {'name': 'Calcium', 'period': 4, 'group': 2, 'charges': [2], 'anion': None},
    #transition metal block 1 start
    'Sc': {'name': 'Scandium', 'period': 4, 'group': 3, 'charges': [3], 'anion': None},
    'Ti': {'name': 'Titanium', 'period': 4, 'group': 4, 'charges': [4, 3], 'anion': None},
    'V': {'name': 'Vanadium', 'period': 4, 'group': 5, 'charges': [5, 4, 3, 2], 'anion': None},
    'Cr': {'name': 'Chromium', 'period': 4, 'group': 6, 'charges': [6, 3, 2], 'anion': None},
    'Mn': {'name': 'Manganese', 'period': 4, 'group': 7, 'charges': [7, 4, 2], 'anion': None},
    'Fe': {'name': 'Iron', 'period': 4, 'group': 8, 'charges': [3, 2], 'anion': None},
    'Co': {'name': 'Cobalt', 'period': 4, 'group': 9, 'charges': [3, 2], 'anion': None},
    'Ni': {'name': 'Nickel', 'period': 4, 'group': 10, 'charges': [2], 'anion': None},
    'Cu': {'name': 'Copper', 'period': 4, 'group': 11, 'charges': [2, 1], 'anion': None},
    'Zn': {'name': 'Zinc', 'period': 4, 'group': 12, 'charges': [2], 'anion': None},
    #transition metal block 1 end
    'Ga': {'name': 'Gallium', 'period': 4, 'group': 13, 'charges': [3], 'anion': None},
    'Ge': {'name': 'Germanium', 'period': 4, 'group': 14, 'charges': [4], 'anion': None},
    'As': {'name': 'Arsenic', 'period': 4, 'group': 15, 'charges': [-3], 'anion': 'arsenide'},
    'Se': {'name': 'Selenium', 'period': 4, 'group': 16, 'charges': [-2], 'anion': 'selenide'},
    'Br': {'name': 'Bromine', 'period': 4, 'group': 17, 'charges': [-1], 'anion': 'bromide'},

    #"Period 5"
    'Rb': {'name': 'Rubidium', 'period': 5, 'group': 1, 'charges': [1], 'anion': None},
    'St': {'name': 'Strontium', 'period': 5, 'group': 2, 'charges': [2], 'anion': None},
     #transition metal block 2 start
    'Y': {'name': 'Yttrium', 'period': 5, 'group': 3, 'charges': [3], 'anion': None},
    'Zr': {'name': 'Zirconium', 'period': 5, 'group': 4, 'charges': [4], 'anion': None},
    'Nb': {'name': 'Niobium', 'period': 5, 'group': 5, 'charges': [5, 3], 'anion': None},
    'Mo': {'name': 'Molybdenum', 'period': 5, 'group': 6, 'charges': [6, 3], 'anion': None},
    'Tc': {'name': 'Technetium', 'period': 5, 'group': 7, 'charges': [6], 'anion': None},
    'Ru': {'name': 'Ruthenium', 'period': 5, 'group': 8, 'charges': [8, 4, 3], 'anion': None},
    'Rh': {'name': 'Rhodium', 'period': 5, 'group': 9, 'charges': [4], 'anion': None},
    'Pd': {'name': 'Palladium', 'period': 5, 'group': 10, 'charges': [4, 2], 'anion': None},
    'Ag': {'name': 'Silver', 'period': 5, 'group': 11, 'charges': [1], 'anion': None},
    'Cd': {'name': 'Cadmium', 'period': 5, 'group': 12, 'charges': [2], 'anion': None},
    #transition metal block 2 end
    'In': {'name': 'Indium', 'period': 5, 'group': 13, 'charges': [3], 'anion': None},
    'Sn': {'name': 'Tin', 'period': 5, 'group': 14, 'charges': [4, 2], 'anion': None},
    'Sb': {'name': 'Antimony', 'period': 5, 'group': 15, 'charges': [-3], 'anion': 'antimide'},
    'Te': {'name': 'Tellurium', 'period': 5, 'group': 16, 'charges': [-2], 'anion': 'telluride'},
    'I': {'name': 'Iodine', 'period': 5, 'group': 17, 'charges': [-1], 'anion': 'iodide'},

    #"Period 6"
    'Cs': {'name': 'Cesium', 'period': 6, 'group': 1, 'charges': [1], 'anion': None},
    'Ba': {'name': 'Barium', 'period': 6, 'group': 2, 'charges': [2], 'anion': None},
    #transition metal block 3 start (we are skipping Lanthanides and Actinides, yeah?)
    'Hf': {'name': 'Hafnium', 'period': 6, 'group': 4, 'charges': [4], 'anion': None},
    'Ta': {'name': 'Tantalum', 'period': 6, 'group': 5, 'charges': [5], 'anion': None},
    'W': {'name': 'Tungsten', 'period': 6, 'group': 6, 'charges': [6], 'anion': None},
    'Re': {'name': 'Rhenium', 'period': 6, 'group': 7, 'charges': [7, 6, 4, 2], 'anion': None},
    'Os': {'name': 'Osmium', 'period': 6, 'group': 8, 'charges': [6, 4, 3], 'anion': None},
    'Ir': {'name': 'Iridium', 'period': 6, 'group': 9, 'charges': [6, 4, 3], 'anion': None},
    'Pt': {'name': 'Platinum', 'period': 6, 'group': 10, 'charges': [6, 4, 2], 'anion': None},
    'Au': {'name': 'Gold', 'period': 6, 'group': 11, 'charges': [3, 2, 1], 'anion': None},
    'Hg': {'name': 'Mercury', 'period': 6, 'group': 12, 'charges': [2, 1], 'anion': None},
    #transition metal block 3 end
    'Tl': {'name': 'Thallium', 'period': 6, 'group': 13, 'charges': [3, 1], 'anion': None},
    'Pb': {'name': 'Lead', 'period': 6, 'group': 14, 'charges': [4, 2], 'anion': None},
    'Bi': {'name': 'Bismuth', 'period': 6, 'group': 15, 'charges': [-3], 'anion': 'bismide'},
    'Po': {'name': 'Polonium', 'period': 6, 'group': 16, 'charges': [-2], 'anion': 'polonide'},
    'At': {'name': 'Astatine', 'period': 6, 'group': 17, 'charges': [-1], 'anion': 'astatide'},
    }

metals = {'Zn', 'Rh', 'Tc', 'Na', 'Ru', 'Mo', 'Ge', 'Sn', 
          'Ca', 'Cu', 'Y', 'Nb', 'Pd', 'Ag', 'In', 'Pt', 
          'W', 'Pb', 'Rb', 'V', 'Fe', 'Cd', 'Cs', 'Hg', 
          'Tl', 'Mn', 'Os', 'St', 'Ir', 'Ta', 'Sc', 'Ba', 
          'Hf', 'Ga', 'Mg', 'Co', 'Ni', 'Ti', 'Li', 'Cr', 
          'Au', 'K', 'Be', 'Zr', 'Re'}

nonmetals = {'Br', 'Al', 'Te', 'F', 'Sb', 'Bi', 'N', 'At', 
             'B', 'Po', 'Se', 'Cl', 'I', 'Si', 'S', 'O', 
             'H', 'C', 'P', 'As'}

covalent ={'H','C','N','B','O','S','Cl','F','P','Se','Br','I'}

prefixes = {
    1: 'mono', 2: 'di', 3: 'tri', 4: 'tetra', 5: 'penta',
    6: 'hexa', 7: 'hepta', 8: 'octa', 9: 'nona', 10: 'deca'
}

roman_numerals = {v: k for v, k in enumerate(['(I)', '(II)', '(III)', '(IV)', '(V)', '(VI)', '(VII)', '(VIII)', '(IX)', '(X)'],1)}

# Helper Functions
def generate_ionic_formula():
    metal = random.choice(list(metals))
    nonmetal = random.choice(list(nonmetals))

    m_charge = random.choice(element_dict[metal]['charges'])
    nm_charge = random.choice(element_dict[nonmetal]['charges'])
    m_sub = abs(nm_charge) // math.gcd(m_charge, abs(nm_charge))
    nm_sub = m_charge // math.gcd(m_charge, abs(nm_charge))

    formula = construct_formula(metal,m_sub,nonmetal,nm_sub)

    if len(element_dict[metal]['charges']) > 1:
        roman = roman_numerals[m_charge]
    else:
        roman = ''
    
    name = f"{element_dict[metal]['name']}{roman} {element_dict[nonmetal]['anion']}".capitalize()
    return formula, name

def construct_formula(term1, sub1, term2, sub2):
    sub1string = '_'+str(sub1) if sub1>1 else ''
    sub2string = '_'+str(sub2) if sub2>1 else ''
    if len(term1) == 2:
        term1string = f"{{{term1}}}"
    else:
        term1string = term1
    if len(term2) == 2:
        term2string = f"{{{term2}}}"
    else:
        term2string = term2
    if sub1string != '' and sub2string != '':
        formula = f"{term1string}{sub1string} \\, {term2string}{sub2string}"
    elif sub1string != '':
        formula = f"{term1string}{sub1string} \\, {term2string}"
    elif sub2string != '':
        formula = f"{term1string} \\, {term2string}{sub2string}"
    else:
        formula = f"{term1string} \\, {term2string}"
    return formula

def generate_covalent_formula():
    e1, e2 = random.sample(list(covalent), 2)
    s1, s2 = random.randint(1, 4), random.randint(1, 4)
    if s1 == s2: s1, s2 = 1, 1  # Avoid dual mono-
    if (s1 == 2 and s2 == 4) or (s2 == 2 and s1 == 4): s1, s2 = s1//2, s2//2
    group1, group2 = element_dict[e1]['group'], element_dict[e2]['group']
    if group1 < group2:
        term1, sub1, term2, sub2 = e1, s1, e2, s2
    elif group1 > group2:
        term1, sub1, term2, sub2 =  e2, s2, e1, s1
    elif element_dict[e1]['period'] > element_dict[e2]['period']:
        term1, sub1, term2, sub2 = e1, s1, e2, s2
    else:
        term1, sub1, term2, sub2 =  e2, s2, e1, s1
    sub1string = '_'+str(sub1) if sub1>1 else ''
    sub2string = '_'+str(sub2) if sub2>1 else ''

    formula = construct_formula(term1, sub1, term2, sub2)
    name = f"{prefixes[sub1].capitalize()}{element_dict[term1]['name'].lower()} {prefixes[sub2].capitalize()}{element_dict[term2]['anion'].lower()}"
    return formula, name


def initialize_session_state():
    if 'formula' not in st.session_state:
        st.session_state.formula = None
    if 'correct_name' not in st.session_state:
        st.session_state.correct_name = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'question_id' not in st.session_state:
        st.session_state.question_id = 0
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None

def check_answer():
    st.session_state.submitted = True
    user_input = st.session_state.user_input  # Get input from the text_input widget
    if user_input and user_input.strip():
        # Clean input
        user_input_clean = user_input.strip().lower().replace(' ','').replace('-','')
        correct_name_clean = st.session_state.correct_name.strip().lower().replace(' ','').replace('-','')
        if user_input_clean == correct_name_clean:
            st.session_state.feedback = "Correct!"
        else:
            st.session_state.feedback = f"Incorrect. The correct name is {st.session_state.correct_name}"
    else:
        st.session_state.feedback = "Please enter an answer before submitting"

def new_question():
    st.session_state.user_answer = None
    st.session_state.submitted = False
    st.session_state.feedback = None
    st.session_state.question_id += 1
    choice = random.choice([True, False])
    st.session_state.formula, st.session_state.correct_name = generate_ionic_formula() if choice else generate_covalent_formula()

# Streamlit App
def main():
    st.title("Compound Naming Practice")

    initialize_session_state()

    # Generate a new problem only if we don't already have one
    if not st.session_state.formula:
        new_question()
    
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.header("Formula: ")
    with col3:
        st.latex(f"\\LARGE{{{st.session_state.formula}}}")

    # Use key parameter to connect the text_input to session state
    st.text_input("Enter the name of the compound", key="user_input", 
                  on_change=None, disabled=st.session_state.submitted)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Check Answer", on_click=check_answer, disabled=st.session_state.submitted)
    with col2:
        st.button("New Question", on_click=new_question)
    
    # Display feedback if available
    if st.session_state.feedback:
        if "Correct" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        elif "Incorrect" in st.session_state.feedback:
            st.error(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

if __name__ == "__main__":
    main()

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

oxygen_prefixes = {
    1: 'mon', 2: 'di', 3: 'tri', 4: 'tetr', 5: 'pent',
    6: 'hex', 7: 'hept', 8: 'oct', 9: 'non', 10: 'dec'
}

roman_numerals = {1: '(I)', 2: '(II)', 3: '(III)', 4: '(IV)', 5: '(V)', 6: '(VI)', 7: '(VII)', 8: '(VIII)', 9: '(IX)', 10: '(X)'}

polyatomic_ions = { 
    'ammonium': {'charges': [1], 'formula': r"\text{N} \, \text{H}_4"},
    'acetate': {'charges':[-1], 'formula': r"\text{C}_2 \, \text{H}_3 \, \text{O}_2"},
    'bicarbonate': {'charges': [-1], 'formula': r"\text{H} \, \text{C} \, \text{O}_3"},
    'bisulfate': {'charges': [-1], 'formula': r"\text{H} \, \text{S} \, \text{O}_4"},
    'chlorate': {'charges': [-1], 'formula': r"\text{Cl} \, \text{O}_2"},
    'citrate': {'charges': [-1], 'formula': r"\text{H}_2 \, \text{C}_6 \, \text{H}_5 \, \text{O}_7"},
    'cyanide': {'charges': [-1], 'formula': r"\text{C} \, \text{N}"},
    'hydroxide': {'charges': [-1], 'formula': r"\text{O} \, \text{H}"},
    'nitrate': {'charges': [-1], 'formula': r"\text{N} \, \text{O}_3"},
    'nitrite': {'charges': [-1], 'formula': r"\text{N} \, \text{O}_2"},
    'perchlorate': {'charges': [-1], 'formula': r"\text{Cl} \, \text{O}_4"},
    'permanganate': {'charges': [-1], 'formula': r"\text{Mn} \, \text{O}_4"},
    'thiocyanate': {'charges': [-1], 'formula': r"\text{S} \, \text{C} \, \text{N}"},
    'carbonate': {'charges': [-2], 'formula': r"\text{C} \, \text{O}_3"},
    'chromate': {'charges': [-2], 'formula': r"\text{Cr} \, \text{O}_4"},
    'dichromate': {'charges': [-2], 'formula': r"\text{Cr}_2 \, \text{O}_7"},
    'sulfate': {'charges': [-2], 'formula': r"\text{S} \, \text{O}_4"},
    'sulfite': {'charges': [-2], 'formula': r"\text{S} \, \text{O}_3"},
    'borate': {'charges': [-3], 'formula': r"\text{B} \, \text{O}_3"},
    'phosphate': {'charges': [-3], 'formula': r"\text{P} \, \text{O}_4"},
}


def order_covalent_elements(e1, s1, e2, s2):
    """Helper function to order covalent elements correctly"""
    group1, group2 = element_dict[e1]['group'], element_dict[e2]['group']
    if group1 < group2:
        return e1, s1, e2, s2
    elif group1 > group2:
        return e2, s2, e1, s1
    elif element_dict[e1]['period'] > element_dict[e2]['period']:
        return e1, s1, e2, s2
    else:
        return e2, s2, e1, s1

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
        formula = f"\\text{{{term1string}}}{sub1string} \\, \\text{{{term2string}}}{sub2string}"
    elif sub1string != '':
        formula = f"\\text{{{term1string}}}{sub1string} \\, \\text{{{term2string}}}"
    elif sub2string != '':
        formula = f"\\text{{{term1string}}} \\, \\text{{{term2string}}}{sub2string}"
    else:
        formula = f"\\text{{{term1string}}} \\, \\text{{{term2string}}}"
    return formula

def make_covalent_name(element_1: str, subscript_1: int, element_2: str, subscript_2: int):
    if subscript_1 == 1:
        term1string = element_dict[element_1]['name'].capitalize()
    elif element_1 == 'O':
        term1string = oxygen_prefixes[subscript_1].capitalize() + element_dict[element_1]['name'].lower()
    else:
        term1string = prefixes[subscript_1].capitalize() + element_dict[element_1]['name'].lower()
    
    if element_2 == 'O':
        term2string = oxygen_prefixes[subscript_2].capitalize() + element_dict[element_2]['anion'].lower()
    else:
        term2string = prefixes[subscript_2].capitalize() + element_dict[element_2]['anion'].lower()
    name = f"{term1string} {term2string}"
    return name


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

def generate_covalent_formula():
    e1, e2 = random.sample(list(covalent), 2)
    s1, s2 = random.randint(1, 4), random.randint(1, 4)
    s1, s2 = s1//math.gcd(s1,s2) , s2//math.gcd(s1,s2)
    group1, group2 = element_dict[e1]['group'], element_dict[e2]['group']
    if group1 < group2:
        term1, sub1, term2, sub2 = e1, s1, e2, s2
    elif group1 > group2:
        term1, sub1, term2, sub2 =  e2, s2, e1, s1
    elif element_dict[e1]['period'] > element_dict[e2]['period']:
        term1, sub1, term2, sub2 = e1, s1, e2, s2
    else:
        term1, sub1, term2, sub2 =  e2, s2, e1, s1

    formula = construct_formula(term1, sub1, term2, sub2)
    name = make_covalent_name(term1, sub1, term2, sub2)
    return formula, name

def generate_polyatomic_formula():
    poly_ion = random.choice(list(polyatomic_ions.keys()))
    if poly_ion == 'ammonium':
        paired_ion = random.choice(list(nonmetals))
    else:
        paired_ion = random.choice(list(metals))
    poly_charge = polyatomic_ions[poly_ion]['charges'][0]
    paired_charge = random.choice(element_dict[paired_ion]['charges'])
    poly_sub = abs(poly_charge) // math.gcd(poly_charge, abs(paired_charge))
    paired_sub = abs(paired_charge) // math.gcd(poly_charge, abs(paired_charge))
    parenth_open = r"\( \,"
    parenth_close = r"\, \)"
    poly_formula = polyatomic_ions[poly_ion]['formula']
    if poly_sub > 1:
        poly_string = r"\left(" + poly_formula + r"\right)_" + str(poly_sub)
    else:
        poly_string = poly_formula
    
    if paired_sub > 1:
        paired_string = f"\\text{{{paired_ion}}}_{{{paired_sub}}}"
    else:
        paired_string = f"\\text{{{paired_ion}}}"
    
    # Order properly (ammonium goes first, otherwise the metal goes first)
    formula = f"{poly_string} \\, {paired_string}" if poly_ion == 'ammonium' else f"{paired_string} \\, {poly_string}"
    
    # Create the name
    if poly_ion == 'ammonium':
        name = f"{poly_ion} {element_dict[paired_ion]['anion']}"
    else:
        # Add Roman numeral for metals with multiple charges
        if len(element_dict[paired_ion]['charges']) > 1:
            roman = roman_numerals[paired_charge]
            name = f"{element_dict[paired_ion]['name']}{roman} {poly_ion}"
        else:
            name = f"{element_dict[paired_ion]['name']} {poly_ion}"
    
    return formula, name.capitalize()


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
    if 'include_polyatomic' not in st.session_state:
        st.session_state.include_polyatomic = False

def on_checkbox_change():
    # This triggers when the checkbox value changes
    new_question()

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
    
    # Use the current include_polyatomic value from session state
    include_polyatomic = st.session_state.include_polyatomic
    
    # Choose a question type based on the include_polyatomic setting
    if include_polyatomic:
        choice = random.randint(1, 3)  # 1=ionic, 2=covalent, 3=polyatomic
    else:
        choice = random.randint(1, 2)  # 1=ionic, 2=covalent
    
    if choice == 1:
        st.session_state.formula, st.session_state.correct_name = generate_ionic_formula()
    elif choice == 2:
        st.session_state.formula, st.session_state.correct_name = generate_covalent_formula()
    else:  # choice == 3
        st.session_state.formula, st.session_state.correct_name = generate_polyatomic_formula()


def create_exploration_page():
    st.title("Chemical Formula Explorer")
    st.write("Select elements and ions to build and visualize chemical formulas")
    
    # Select formula type
    formula_type = st.selectbox(
        "Select Formula Type",
        ["Covalent Compound", "Ionic Compound (Monatomic)", "Ionic Compound (with Polyatomic Ion)"]
    )
    
    if formula_type == "Covalent Compound":
        # Select two covalent elements
        col1, col2 = st.columns(2)
        with col1:
            element1 = st.selectbox("First Element", 
                                   sorted([e for e in covalent], 
                                          key=lambda x: element_dict[x]['name']))
            st.write(f"{element_dict[element1]['name']}")
            subscript1 = st.number_input("Subscript", 1, 10, 1, key="sub1")
        with col2:
            element2 = st.selectbox("Second Element", 
                                   sorted([e for e in covalent if e != element1], 
                                          key=lambda x: element_dict[x]['name']))
            st.write(f"{element_dict[element2]['name']}")
            subscript2 = st.number_input("Subscript", 1, 10, 1, key="sub2")
            
        # Calculate formula and name
        term1, sub1, term2, sub2 = order_covalent_elements(element1, subscript1, element2, subscript2)
        formula = construct_formula(term1, sub1, term2, sub2)
        name = make_covalent_name(term1, sub1, term2, sub2)
        
    elif formula_type == "Ionic Compound (Monatomic)":
        # Select metal and nonmetal
        col1, col2 = st.columns(2)
        with col1:
            metal = st.selectbox("Metal", 
                               sorted([e for e in metals], 
                                      key=lambda x: element_dict[x]['name']))
            st.write(f"{element_dict[metal]['name']}")
            
            if len(element_dict[metal]['charges']) > 1:
                metal_charge = st.selectbox(
                    f"Charge", 
                    sorted(element_dict[metal]['charges'])
                )
            else:
                metal_charge = element_dict[metal]['charges'][0]
                st.write(f"Charge: +{metal_charge}")
        
        with col2:
            nonmetal = st.selectbox("Nonmetal", 
                                   sorted([e for e in nonmetals if element_dict[e]['anion'] is not None], 
                                          key=lambda x: element_dict[x]['name']))
            st.write(f"{element_dict[nonmetal]['name']}")
            nonmetal_charge = element_dict[nonmetal]['charges'][0]
            st.write(f"Charge: {nonmetal_charge}")
        
        # Calculate formula
        m_sub = abs(nonmetal_charge) // math.gcd(metal_charge, abs(nonmetal_charge))
        nm_sub = metal_charge // math.gcd(metal_charge, abs(nonmetal_charge))
        formula = construct_formula(metal, m_sub, nonmetal, nm_sub)
        
        # Calculate name
        if len(element_dict[metal]['charges']) > 1:
            roman = roman_numerals[metal_charge]
            name = f"{element_dict[metal]['name']}{roman} {element_dict[nonmetal]['anion']}".capitalize()
        else:
            name = f"{element_dict[metal]['name']} {element_dict[nonmetal]['anion']}".capitalize()
    
    else:  # Ionic Compound with Polyatomic Ion
        # First determine if we're using ammonium (cation) or other polyatomic ions (anion)
        use_ammonium = st.checkbox("Use Ammonium (NH₄⁺) as the Cation", False)
        
        if use_ammonium:
            # Ammonium + nonmetal
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Cation: Ammonium**")
                st.write("Formula: NH₄⁺")
                st.write("Charge: +1")
                poly_ion = "ammonium"
                poly_charge = polyatomic_ions[poly_ion]['charges'][0]
            with col2:
                nonmetal = st.selectbox("Anion (Nonmetal)", 
                                       sorted([e for e in nonmetals if element_dict[e]['anion'] is not None], 
                                              key=lambda x: element_dict[x]['name']))
                st.write(f"{element_dict[nonmetal]['name']}")
                nonmetal_charge = element_dict[nonmetal]['charges'][0]
                st.write(f"Charge: {nonmetal_charge}")
            
            # Calculate formula
            poly_sub = abs(nonmetal_charge) // math.gcd(poly_charge, abs(nonmetal_charge))
            nm_sub = poly_charge // math.gcd(poly_charge, abs(nonmetal_charge))
            
            poly_formula = polyatomic_ions[poly_ion]['formula']
            if poly_sub > 1:
                poly_string = r"\left(" + poly_formula + r"\right)_" + str(poly_sub)
            else:
                poly_string = poly_formula
            
            if nm_sub > 1:
                nm_string = f"\\text{{{nonmetal}}}_{{{nm_sub}}}"
            else:
                nm_string = f"\\text{{{nonmetal}}}"
            
            formula = f"{poly_string} \\, {nm_string}"
            name = f"Ammonium {element_dict[nonmetal]['anion']}".capitalize()
            
        else:
            # Metal + polyatomic anion
            col1, col2 = st.columns(2)
            with col1:
                metal = st.selectbox("Cation (Metal)", 
                                   sorted([e for e in metals], 
                                          key=lambda x: element_dict[x]['name']))
                st.write(f"{element_dict[metal]['name']}")
                
                if len(element_dict[metal]['charges']) > 1:
                    metal_charge = st.selectbox(
                        f"Charge", 
                        sorted(element_dict[metal]['charges'])
                    )
                else:
                    metal_charge = element_dict[metal]['charges'][0]
                    st.write(f"Charge: +{metal_charge}")
                    
            with col2:
                # Filter out ammonium for polyatomic anions
                poly_options = {k: v for k, v in polyatomic_ions.items() if k != "ammonium"}
                poly_ion = st.selectbox("Anion (Polyatomic)", sorted(list(poly_options.keys())))
                poly_charge = polyatomic_ions[poly_ion]['charges'][0]
                st.write(f"Charge: {poly_charge}")
            
            # Calculate formula
            metal_sub = abs(poly_charge) // math.gcd(metal_charge, abs(poly_charge))
            poly_sub = metal_charge // math.gcd(metal_charge, abs(poly_charge))
            
            if metal_sub > 1:
                metal_string = f"\\text{{{metal}}}_{{{metal_sub}}}"
            else:
                metal_string = f"\\text{{{metal}}}"
            
            poly_formula = polyatomic_ions[poly_ion]['formula']
            if poly_sub > 1:
                poly_string = r"\left(" + poly_formula + r"\right)_" + str(poly_sub)
            else:
                poly_string = poly_formula
            
            formula = f"{metal_string} \\, {poly_string}"
            
            # Calculate name
            if len(element_dict[metal]['charges']) > 1:
                roman = roman_numerals[metal_charge]
                name = f"{element_dict[metal]['name']}{roman} {poly_ion}".capitalize()
            else:
                name = f"{element_dict[metal]['name']} {poly_ion}".capitalize()
    
    # Display the results
    st.markdown("---")
    st.subheader("Result:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Formula:**")
        st.latex(f"\\LARGE{{{formula}}}")
    
    with col2:
        st.markdown("**Name:**")
        st.markdown(f"### {name}")
    
    st.markdown("---")
    st.write("Note: This tool follows standard chemical naming conventions. In some cases, alternative names may be used in different contexts.")

def practice_quiz_page():
    st.title("Compound Naming Practice")
    
    initialize_session_state()
    
    # Use st.expander to hide settings in a collapsible section
    with st.expander("Settings", expanded=False):
        st.checkbox("Include Polyatomic Ions?", 
                    value=st.session_state.include_polyatomic,
                    key="include_polyatomic", 
                    on_change=on_checkbox_change)

    # Generate a new problem only if we don't already have one
    if not st.session_state.formula:
        new_question()
    
    st.markdown("### Name this compound:")
    st.latex(f"\\LARGE{{{st.session_state.formula}}}")
    
    # For testing only - Remove in production
    if st.session_state.get('show_answer', False):
        st.info(f"Answer: {st.session_state.correct_name}")
    
    # Use key parameter to connect the text_input to session state
    st.text_input("Enter the name of the compound", 
                  key="user_input", 
                  disabled=st.session_state.submitted)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("Check Answer", 
                  on_click=check_answer, 
                  disabled=st.session_state.submitted)
    with col2:
        st.button("New Question", 
                  on_click=new_question)
    with col3:
        # For testing only - Remove in production
        st.checkbox("Show answers (for testing)", key="show_answer")
    
    # Display feedback if available
    if st.session_state.feedback:
        if "Correct" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        elif "Incorrect" in st.session_state.feedback:
            st.error(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

def main():
    # Add tabs for quiz and explorer modes
    tab1, tab2 = st.tabs(["Practice Quiz", "Formula Explorer"])
    
    with tab1:
        practice_quiz_page()
    
    with tab2:
        create_exploration_page()

if __name__ == "__main__":
    main()
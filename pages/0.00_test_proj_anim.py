import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.generators.linear_motion_generator import LinearMotionGenerator
generator = LinearMotionGenerator()
x, v_f,v_i,t = generator.no_acc_eq_nums("Easy")
print(f"{x}, {v_f}, {v_i}, {t}")
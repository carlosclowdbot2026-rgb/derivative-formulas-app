# -*- coding: utf-8 -*-
"""
Derivative Formula Learning App
Run: streamlit run derivative_app.py
"""

import streamlit as st
import random

# Page config
st.set_page_config(
    page_title="Derivative Formulas",
    page_icon="d/dx",
    layout="centered"
)

# Formula database
formulas = {
    "Basic": {
        "Power Rule": {"formula": "d/dx(x^n) = n*x^(n-1)", "example": "d/dx(x^3) = 3x^2"},
        "Constant": {"formula": "d/dx(C) = 0", "example": "d/dx(5) = 0"},
        "Linear": {"formula": "d/dx(kx) = k", "example": "d/dx(3x) = 3"},
    },
    "Trigonometric": {
        "Sine": {"formula": "d/dx(sin x) = cos x", "example": "d/dx(sin 2x) = 2cos 2x"},
        "Cosine": {"formula": "d/dx(cos x) = -sin x", "example": "d/dx(cos 3x) = -3sin 3x"},
        "Tangent": {"formula": "d/dx(tan x) = sec^2 x", "example": "d/dx(tan x^2) = 2x sec^2(x^2)"},
    },
    "Exponential": {
        "e^x": {"formula": "d/dx(e^x) = e^x", "example": "d/dx(e^2x) = 2e^2x"},
        "a^x": {"formula": "d/dx(a^x) = a^x * ln a", "example": "d/dx(2^x) = 2^x * ln 2"},
    },
    "Logarithmic": {
        "ln x": {"formula": "d/dx(ln x) = 1/x", "example": "d/dx(ln 2x) = 1/x"},
        "log_a x": {"formula": "d/dx(log_a x) = 1/(x * ln a)", "example": "d/dx(log_2 x) = 1/(x * ln 2)"},
    },
    "Inverse Trig": {
        "arcsin": {"formula": r"\frac{d}{dx}(\arcsin x) = \frac{1}{\sqrt{1-x^2}}", "example": r"\frac{d}{dx}(\arcsin 2x) = \frac{2}{\sqrt{1-4x^2}}"},
        "arccos": {"formula": r"\frac{d}{dx}(\arccos x) = -\frac{1}{\sqrt{1-x^2}}", "example": r"\frac{d}{dx}(\arccos x^2) = -\frac{2x}{\sqrt{1-x^4}}"},
        "arctan": {"formula": r"\frac{d}{dx}(\arctan x) = \frac{1}{1+x^2}", "example": r"\frac{d}{dx}(\arctan 3x) = \frac{3}{1+9x^2}"},
        "arccot": {"formula": r"\frac{d}{dx}(\arccot x) = -\frac{1}{1+x^2}", "example": r"\frac{d}{dx}(\arccot \frac{x}{2}) = -\frac{1}{2(1+\frac{x^2}{4})}"},
    },
    "Rules": {
        "Sum Rule": {"formula": "d/dx(f +/- g) = f' +/- g'", "example": "d/dx(x^2 + sin x) = 2x + cos x"},
        "Product Rule": {"formula": "d/dx(fg) = f'g + fg'", "example": "d/dx(x * sin x) = sin x + x cos x"},
        "Quotient Rule": {"formula": "d/dx(f/g) = (f'g - fg')/g^2", "example": "d/dx(sin x / x) = (x cos x - sin x)/x^2"},
        "Chain Rule": {"formula": "d/dx(f(g(x))) = f'(g) * g'(x)", "example": "d/dx(sin(x^2)) = cos(x^2) * 2x"},
    },
}

# Sidebar navigation
st.sidebar.title("d/dx Formulas")
mode = st.sidebar.radio("Select Mode", ["Formula Cards", "Random Quiz", "Practice Quiz"])

if mode == "Formula Cards":
    st.title("Formula Cards")
    category = st.selectbox("Select Category", list(formulas.keys()))
    
    for name, data in formulas[category].items():
        with st.expander(f"{name}"):
            st.latex(data["formula"])
            st.caption(f"Example: {data['example']}")

elif mode == "Random Quiz":
    st.title("Random Quiz")
    
    # Initialize session state
    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = None
    
    # Get new formula
    if st.button("Get New Formula"):
        cat = random.choice(list(formulas.keys()))
        name = random.choice(list(formulas[cat].keys()))
        st.session_state.quiz_question = {
            "category": cat,
            "name": name,
            "formula": formulas[cat][name]["formula"],
            "example": formulas[cat][name]["example"]
        }
    
    # Show current question
    if st.session_state.quiz_question:
        q = st.session_state.quiz_question
        st.markdown(f"**Category:** {q['category']}")
        st.markdown(f"**Formula:** {q['name']}")
        st.info("Write the formula on paper, then click below to check!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show Formula"):
                st.success(f"**{q['formula']}**")
        with col2:
            if st.button("Show Example"):
                st.info(f"Example: {q['example']}")

elif mode == "Practice Quiz":
    st.title("Practice Quiz")
    
    questions = [
        {"q": "d/dx(x^4) = ?", "a": "4x^3", "options": ["4x^3", "x^4", "4x^5", "x^3"]},
        {"q": "d/dx(sin x) = ?", "a": "cos x", "options": ["-sin x", "cos x", "sin x", "-cos x"]},
        {"q": "d/dx(e^x) = ?", "a": "e^x", "options": ["e^x", "x*e^(x-1)", "x*e^x", "ln x"]},
        {"q": "d/dx(ln x) = ?", "a": "1/x", "options": ["x", "1/x", "ln x", "0"]},
        {"q": "d/dx(2^x) = ?", "a": "2^x * ln 2", "options": ["2^x", "2^x * ln 2", "x*2^(x-1)", "2^x / ln 2"]},
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.subheader(f"Question {i+1}")
        st.write(q["q"])
        choice = st.radio("Select answer", q["options"], key=f"q{i}")
        if st.button(f"Check Q{i+1}", key=f"btn{i}"):
            if choice == q["a"]:
                st.success("Correct!")
                score += 1
            else:
                st.error(f"Wrong! Answer: {q['a']}")
    
    if st.button("Show Score"):
        st.success(f"Score: {score}/{len(questions)}")

# Footer
st.markdown("---")
st.caption("Derivative Formula Learning App | Calculus I")

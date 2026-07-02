import os
import streamlit as st

# API key ko environment variable se uthaein
api_key = os.environ.get("GEMINI_API_KEY")

# Title set karna
st.title("Enterprise AI Insights Studio")

if not api_key:
    st.error("GEMINI_API_KEY set nahi hai! Kripya Render settings check karein.")
else:
    import pandas as pd
    
    # Safe library import with fallback
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        LIB_LOADED = True
    except ImportError:
        LIB_LOADED = False
        st.error("Google Generative AI library install nahi hai.")

    st.write("Let's start building! For help and inspiration, head over to docs.")
    
    # Yahan aap apna baaki ka AI logic add kar sakti hain
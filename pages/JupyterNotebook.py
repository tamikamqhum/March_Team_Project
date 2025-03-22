import streamlit as st

st.set_page_config(page_title="Jupyter Notebook Viewer", layout="wide")

st.title("📓 Jupyter Notebook Viewer")
st.markdown("This page embeds our Jupyter Notebook using **nbviewer**.")

notebook_url = "https://nbviewer.org/github/Hasnain-S1/March_Team_Project-H/blob/main/jupyter_notebooks/HS-Notebook_Template.ipynb"

st.markdown(f"### 📜 View the Notebook Below:")
st.markdown(f"[🔗 Open in a new tab]({notebook_url})", unsafe_allow_html=True)

# Embed nbviewer iframe
st.components.v1.iframe(notebook_url, height=800, scrolling=True)

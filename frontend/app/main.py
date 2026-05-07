import streamlit as st

st.set_page_config(
    page_title="ExpenseFlow",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
        .block-container {
            max-width: 520px;
            padding-top: 5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = None

if st.session_state.get("token"):
    st.switch_page("pages/home.py")
else:
    st.switch_page("pages/login.py")
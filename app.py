import streamlit as st

st.set_page_config(
    page_title="Stock Assistant",
    page_icon="📈",
    layout="wide"
)

# Hide streamlit elements and file names
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .reportview-container {margin-top: -2em;}
    .stApp > header {height: 0rem;}
    .stApp > div:first-child {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Stock Assistant")
    
    page = st.radio(
        "",
        [
            "Chat",
            "Technical Analysis",
            "Stock Information", 
            "AI Assistant",
            "Document Summary",
            "Document Q&A"
        ],
        label_visibility="collapsed"
    )

if page == "Chat":
    exec(open("pages/chat.py").read())
elif page == "Technical Analysis":
    exec(open("pages/technical_analysis.py").read())
elif page == "Stock Information":
    exec(open("pages/stock_info.py").read())
elif page == "AI Assistant":
    exec(open("pages/ai_assistant.py").read())
elif page == "Document Summary":
    exec(open("pages/doc_summary.py").read())
elif page == "Document Q&A":
    exec(open("pages/document_qa.py").read())

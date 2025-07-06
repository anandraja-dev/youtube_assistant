import langchain_helper as lch
import streamlit as st
import textwrap

st.set_page_config(layout="wide")

st.title("Youtube Assistant")

st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{
        background-color: #f0f2f6;
        padding: 20px;
    }}
    [data-testid="stSidebarNav"] {{
        display: none;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.text_area(
            label="What is the YouTube video URL?",
            max_chars=50
        )
        query = st.text_area(
            label="Ask me about the video?",
            max_chars=50,
            key="query"
        )
        submit_button = st.form_submit_button(label='Submit')

if query and youtube_url:
    with st.spinner("Fetching response..."):
        db = lch.create_vector_db_from_youtube_url(youtube_url)
        response = lch.get_response_from_query(db, query)
        st.subheader("Answer:")
        st.markdown(f"""
        <div style="
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {response}
        </div>
        """, unsafe_allow_html=True)
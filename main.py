import langchain_helper as lch
import streamlit as st
import textwrap
import time

st.set_page_config(
    page_title="Local YouTube Assistant", 
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Local YouTube Assistant")
st.markdown("*Powered by your local Ollama models - 100% private!*")

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        padding: 10px;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    .success-box {
        border: 1px solid #28a745;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #d4edda;
        color: #155724;
    }
    .info-box {
        border: 1px solid #17a2b8;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .error-box {
        border: 1px solid #dc3545;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Model selection
    model_choice = st.selectbox(
        "Select Ollama Model:",
        options=["gpt-oss:20b", "llama3.2-vision:11b", "llama3.1:8b"],
        index=0,
        help="Choose which local model to use for analysis"
    )
    
    st.info(f"💡 **Your Setup:**\n- Model: {model_choice}\n- Privacy: 100% Local\n- Cost: $0 per query")
    
    with st.form(key='youtube_form'):
        youtube_url = st.text_input(
            label="🔗 YouTube Video URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste the full YouTube video URL here"
        )
        
        # Language selection
        language = st.selectbox(
            "🌐 Transcript Language:",
            options=[("English", "en"), ("Tamil", "ta"), ("Hindi", "hi"), ("Spanish", "es")],
            format_func=lambda x: x[0],
            index=0
        )
        
        query = st.text_area(
            label="❓ Your Question:",
            placeholder="What is this video about?",
            height=100,
            help="Ask anything about the video content"
        )
        
        submit_button = st.form_submit_button(
            label='🚀 Analyze Video',
            type="primary"
        )

# Main content area
col1, col2 = st.columns([2, 1])

with col2:
    st.header("📊 Model Status")
    
    # Check Ollama status
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            st.markdown('<div class="success-box">✅ Ollama Server: Online</div>', unsafe_allow_html=True)
            models = response.json().get('models', [])
            available_models = [m['name'] for m in models]
            st.write("**Available Models:**")
            for model in available_models:
                if model in ["gpt-oss:20b", "llama3.2-vision:11b"]:
                    st.write(f"✅ {model}")
                else:
                    st.write(f"ℹ️ {model}")
        else:
            st.markdown('<div class="error-box">❌ Ollama Server: Offline</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="error-box">❌ Cannot connect to Ollama</div>', unsafe_allow_html=True)
        st.write("Make sure Ollama is running!")

with col1:
    if submit_button and youtube_url and query:
        # Validate YouTube URL
        if "youtube.com/watch" not in youtube_url and "youtu.be/" not in youtube_url:
            st.error("❌ Please enter a valid YouTube URL")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Get video info
                status_text.text("📺 Getting video information...")
                progress_bar.progress(10)
                video_info = lch.get_video_info(youtube_url)
                
                st.markdown(f"""
                <div class="info-box">
                    <h4>📺 Video Information</h4>
                    <strong>Title:</strong> {video_info['title']}<br>
                    <strong>Author:</strong> {video_info['author']}<br>
                    <strong>Transcript Length:</strong> {video_info['length']:,} characters
                </div>
                """, unsafe_allow_html=True)
                
                # Step 2: Create vector database
                status_text.text("🔍 Processing transcript and creating embeddings...")
                progress_bar.progress(30)
                
                db = lch.create_vector_db_from_youtube_url(youtube_url, language[1])
                progress_bar.progress(60)
                
                # Step 3: Get response
                status_text.text(f"🤖 Analyzing with {model_choice}...")
                progress_bar.progress(80)
                
                start_time = time.time()
                response = lch.get_response_from_query(db, query, k=4, model_name=model_choice)
                end_time = time.time()
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Display results
                st.subheader("🎯 Answer:")
                st.markdown(f"""
                <div class="success-box">
                    {response}
                </div>
                """, unsafe_allow_html=True)
                
                # Performance metrics
                st.markdown(f"""
                <div class="info-box">
                    <strong>⚡ Performance:</strong><br>
                    Response Time: {end_time - start_time:.1f} seconds<br>
                    Model: {model_choice}<br>
                    Language: {language[0]}<br>
                    Privacy: 100% Local Processing
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 **Troubleshooting:**\n- Check if Ollama is running\n- Verify the YouTube URL is accessible\n- Ensure the video has captions/transcript")

    elif submit_button:
        if not youtube_url:
            st.warning("⚠️ Please enter a YouTube URL")
        if not query:
            st.warning("⚠️ Please enter a question")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>
        🔒 <strong>100% Private:</strong> Your data never leaves your machine<br>
        💰 <strong>Zero Cost:</strong> No API fees with local processing<br>
        ⚡ <strong>Your Models:</strong> GPT-OSS 20B + Llama3.2-Vision 11B
    </small>
</div>
""", unsafe_allow_html=True)
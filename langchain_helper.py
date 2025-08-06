# ================================
# langchain_helper.py - MODIFIED for Local Ollama
# ================================

from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_community.llms import Ollama
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Use HuggingFace embeddings (works offline)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

def create_vector_db_from_youtube_url(video_url: str, language: str = "en") -> FAISS:
    """Create vector database from YouTube video transcript"""
    try:
        # Load transcript in the preferred language
        print(f"🔍 Loading transcript in '{language}'...")
        loader = YoutubeLoader.from_youtube_url(video_url, language=[language])
        transcript = loader.load()

        if not transcript:
            raise ValueError(f"No transcript found for language '{language}'")
        
        print(f"✅ Transcript loaded successfully! Length: {len(transcript[0].page_content)} characters")

    except Exception as e:
        print(f"⚠️ Failed to load '{language}' transcript: {e}")
        if language != "en":
            print("🔁 Falling back to English...")
            loader = YoutubeLoader.from_youtube_url(video_url, language=["en"])
            transcript = loader.load()
        else:
            raise Exception(f"Failed to load transcript: {e}")

    # Split the transcript into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,  # Increased overlap for better context
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    docs = text_splitter.split_documents(transcript)
    
    print(f"📝 Created {len(docs)} document chunks")

    # Create FAISS vector database
    print("🔍 Creating vector embeddings...")
    db = FAISS.from_documents(docs, embeddings)
    print("✅ Vector database created successfully!")

    return db

def get_response_from_query(db, query, k=4, model_name="gpt-oss:20b"):
    """Get response from query using local Ollama model"""
    
    print(f"🔍 Searching for relevant chunks (k={k})...")
    docs = db.similarity_search(query, k=k)
    docs_page_content = "\n\n".join([f"Chunk {i+1}:\n{d.page_content}" for i, d in enumerate(docs)])
    
    print(f"📄 Found {len(docs)} relevant chunks")
    
    # Initialize local Ollama LLM
    llm = Ollama(
        model=model_name,
        base_url="http://localhost:11434",
        temperature=0.3,  # Lower temperature for more focused answers
    )

    # Enhanced prompt template for better responses
    prompt_template = PromptTemplate(
        input_variables=["question", "docs"],
        template="""You are an intelligent YouTube video assistant. Your task is to answer questions about YouTube videos based on their transcripts.

CONTEXT (Video Transcript Chunks):
{docs}

USER QUESTION: {question}

INSTRUCTIONS:
1. Analyze the provided transcript chunks carefully
2. Answer the question using ONLY information from the transcript
3. Be specific and detailed in your response
4. If the question asks for examples, quotes, or specific details, include them from the transcript
5. If you cannot find relevant information in the transcript, say "I don't have enough information in the transcript to answer this question"
6. Structure your answer clearly with bullet points or paragraphs as appropriate

ANSWER:""",
    )
    
    # Create the chain
    chain = prompt_template | llm
    
    print(f"🤖 Sending query to {model_name}...")
    print("⏳ This may take 30-60 seconds for detailed responses...")
    
    try:
        response = chain.invoke({"question": query, "docs": docs_page_content})
        print("✅ Response generated successfully!")
        return response.strip()
    except Exception as e:
        error_msg = f"Error getting response from {model_name}: {str(e)}"
        print(f"❌ {error_msg}")
        return f"Sorry, I encountered an error: {error_msg}. Please try again or check if Ollama is running."

def get_video_info(video_url: str) -> dict:
    """Extract basic video information"""
    try:
        loader = YoutubeLoader.from_youtube_url(video_url, language=["en"])
        transcript = loader.load()
        if transcript:
            metadata = transcript[0].metadata
            return {
                "title": metadata.get("title", "Unknown Title"),
                "author": metadata.get("author", "Unknown Author"),
                "length": len(transcript[0].page_content),
                "source": metadata.get("source", video_url)
            }
    except:
        pass
    return {"title": "Unknown", "author": "Unknown", "length": 0, "source": video_url}
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from typing import List

load_dotenv()

# Initialize Gemini embedding model
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
# video_url = "https://www.youtube.com/watch?v=wr8gJMj3ODw"
def create_vector_db_from_youtube_url(video_url: str, language: str = "ta")->FAISS:
    try:
        # Attempt to load transcript in the preferred language (Tamil)
        loader = YoutubeLoader.from_youtube_url(video_url, language=[language])
        transcript = loader.load()

        if not transcript:
            raise ValueError(f"No transcript found for language '{language}'")

    except Exception as e:
        print(f"⚠️ Failed to load '{language}' transcript: {e}")
        print("🔁 Falling back to English...")
        loader = YoutubeLoader.from_youtube_url(video_url, language=["en"])
        transcript = loader.load()

    # Split the transcript into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    # Create FAISS vector database
    db = FAISS.from_documents(docs, embeddings)

    return db  #  return the vector store
def get_response_from_query(db,query,k=4):

    docs= db.similarity_search(query, k=k)
    docs_page_content = "".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # "gemini-2.0-flash" does not exist

    # Create the prompt template
    prompt_template_name = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )
    name_chain = prompt_template_name | llm
    response = name_chain.invoke({"question": query, "docs": docs_page_content})
    return str(response.content).strip()




# create_vector_db_from_youtube_url(video_url, language="ta")

# vector_db: FAISS = create_vector_db_from_youtube_url(video_url, language="ta")

# print(create_vector_db_from_youtube_url(video_url))
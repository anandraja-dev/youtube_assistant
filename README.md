"""
# 🎬 Local YouTube Assistant

A powerful YouTube video analysis tool that runs **100% locally** using Ollama models. Ask questions about any YouTube video and get intelligent answers based on the video's transcript - completely private and free!

## 🌟 Features

- ✅ **100% Local Processing** - No data sent to external APIs
- 🤖 **Multiple Model Support** - Works with your Ollama models
- 🌐 **Multi-language Transcripts** - English, Tamil, Hindi, Spanish support  
- 🔒 **Complete Privacy** - All processing happens on your machine
- 💰 **Zero API Costs** - No usage fees or rate limits
- ⚡ **Optimized for Your Setup** - Works great with 32GB RAM

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ollama installed and running
- Your models: `gpt-oss:20b` and `llama3.2-vision:11b`

### Installation

1. **Clone/Download the project**
   ```bash
   git clone <repository-url>
   cd youtube-assistant-local
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Ollama is running**
   ```bash
   ollama list  # Should show your models
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 💡 Usage

1. **Enter YouTube URL** - Paste any YouTube video URL
2. **Select Language** - Choose transcript language (defaults to English)
3. **Choose Model** - Select from your available Ollama models
4. **Ask Question** - Type your question about the video
5. **Get Answer** - Receive detailed analysis in seconds!

## 🎯 Perfect For

- **Education** - Analyze educational videos and lectures
- **Research** - Extract insights from conference talks
- **Business** - Analyze product demos and presentations  
- **Content Creation** - Research competitor content
- **Personal Learning** - Get summaries of long videos

## 🔧 Technical Details

**Models Used:**
- **GPT-OSS 20B** - Primary analysis and reasoning
- **Llama3.2-Vision 11B** - Future multimodal features
- **HuggingFace Embeddings** - Local text embeddings

**Performance:**
- **RAM Usage**: ~15GB for GPT-OSS model
- **Response Time**: 30-90 seconds depending on complexity
- **Privacy**: 100% local processing
- **Cost**: $0 per query

## 🛠️ Troubleshooting

**Ollama Connection Issues:**
```bash
# Check if Ollama is running
ollama list

# Restart Ollama if needed
# Then restart the Streamlit app
```

**Model Not Found:**
```bash
# Pull required model
ollama pull gpt-oss:20b
```

**Slow Responses:**
- First query is always slower (model loading)
- Keep Ollama running in background
- Use shorter questions for faster responses

## 🚀 Advanced Features

- **Custom Models** - Easy to add new Ollama models
- **Batch Processing** - Analyze multiple videos
- **Export Results** - Save responses for later use
- **Performance Monitoring** - Track response times

## 🎉 Why This Rocks

1. **Complete Privacy** - Perfect for confidential content
2. **No API Limits** - Unlimited queries
3. **Works Offline** - No internet needed after setup
4. **Cost Effective** - No ongoing subscription fees
5. **Your Hardware** - Optimized for your 32GB RAM setup

---

*Built with ❤️ for local AI enthusiasts*
"""
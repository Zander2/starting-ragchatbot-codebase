# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation and Setup
```bash
# Install uv package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
uv sync

# Create environment file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the Application
```bash
# Quick start (recommended)
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000

# Access the application
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Development Environment
```bash
# Run with Python directly (for debugging)
cd backend
export PATH="$HOME/.local/bin:$PATH"
uv run python app.py

# Check dependencies
uv tree

# Clear vector database (for fresh start)
rm -rf backend/chroma_db

# Debug mode with more verbose logging
cd backend && PYTHONPATH=. uv run python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from app import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
"
```

## Architecture Overview

This is a **Retrieval-Augmented Generation (RAG) system** for querying course materials using semantic search and AI responses.

### Core Architecture Pattern
The system uses a **tool-based RAG approach** where:
1. Claude AI intelligently decides when to search vs. use general knowledge
2. Search is performed only when course-specific information is needed
3. Vector search provides context for AI response generation

### Key Components

**RAG Orchestration (`backend/rag_system.py`)**
- Central coordinator managing all system components
- Handles query processing: prompt building → AI generation → tool execution → response synthesis
- Manages conversation history via `SessionManager`

**AI Generation with Tools (`backend/ai_generator.py`)**
- Interfaces with Anthropic Claude API using tool calling
- Handles two-phase tool execution: tool request → tool execution → final response
- Uses static system prompt optimized for educational content

**Vector Search System (`backend/vector_store.py` + `backend/search_tools.py`)**
- ChromaDB for semantic similarity search
- Course-aware search with title and lesson filtering
- `CourseSearchTool` formats results and tracks sources for UI display

**Document Processing Pipeline (`backend/document_processor.py`)**
- Processes course transcripts from `docs/*.txt` files
- Extracts structured metadata: course titles, lessons, instructors
- Creates overlapping text chunks optimized for semantic search

### Data Models (`backend/models.py`)
- `Course`: Contains title, lessons, metadata
- `Lesson`: Sequential lessons with titles and optional links
- `CourseChunk`: Text chunks with course/lesson context for vector storage

### Configuration (`backend/config.py`)
Key settings:
- `CHUNK_SIZE: 800` - Text chunk size for vector storage
- `CHUNK_OVERLAP: 100` - Overlap between chunks
- `MAX_RESULTS: 5` - Search results returned
- `MAX_HISTORY: 2` - Conversation messages to remember
- `ANTHROPIC_MODEL: "claude-sonnet-4-20250514"` - Claude model version
- `CHROMA_PATH: "./chroma_db"` - ChromaDB storage location
- `EMBEDDING_MODEL: "all-MiniLM-L6-v2"` - Sentence transformer model

## Development Patterns

### Adding New Course Documents
1. Place `.txt`, `.pdf`, or `.docx` files in `docs/` folder
2. Application auto-loads on startup via `app.py:startup_event()`
3. Document processor extracts course structure and creates vector embeddings

### Modifying Search Behavior
- **Search logic**: `backend/search_tools.py:CourseSearchTool.execute()`
- **Vector operations**: `backend/vector_store.py:VectorStore.search()`
- **Tool definitions**: `backend/search_tools.py:CourseSearchTool.get_tool_definition()`

### Session Management
- In-memory conversation history (not persistent)
- Configurable via `MAX_HISTORY` setting
- Session lifecycle managed in `backend/session_manager.py`

### Frontend Integration
- Vanilla JavaScript frontend in `frontend/`
- API communication via `/api/query` and `/api/courses` endpoints
- Real-time chat interface with source attribution

### Testing
- No testing framework is currently configured
- To add tests, consider adding pytest to dependencies: `uv add pytest`
- Test files should follow pattern: `test_*.py` or `*_test.py`

### Common Development Issues
- **Missing API key**: Ensure ANTHROPIC_API_KEY is set in `.env`
- **ChromaDB errors**: Clear database with `rm -rf backend/chroma_db` and restart
- **Document processing failures**: Check file permissions and formats in `docs/`
- **Port conflicts**: Default port 8000 can be changed in run command

## Required Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required - get from console.anthropic.com
```

## File Structure Context

- `backend/app.py` - FastAPI server and API endpoints
- `backend/rag_system.py` - Main orchestration logic
- `backend/ai_generator.py` - Claude API integration with tool calling
- `backend/vector_store.py` - ChromaDB vector database operations
- `backend/search_tools.py` - Search tool implementation for Claude
- `backend/document_processor.py` - Course document parsing and chunking
- `docs/` - Course material files (auto-loaded on startup)
- `frontend/` - Web interface (served by FastAPI static files)

The system is designed for educational content querying with intelligent search decisions and maintains conversation context across queries.
- Always use uv to run the server do not use pip direcly
- make sure to use uv to manage all dependencies
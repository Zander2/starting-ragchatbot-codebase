# RAG System Query Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as FastAPI
    participant R as RAGSystem
    participant AI as AIGenerator
    participant T as ToolManager
    participant V as VectorStore
    participant C as Claude API

    U->>F: Types query & clicks send
    F->>F: Disable UI, show loading
    F->>A: POST /api/query

    A->>A: Create session if needed
    A->>R: rag_system.query()

    R->>R: Build prompt
    R->>R: Get conversation history
    R->>AI: generate_response()

    AI->>AI: Build system prompt
    AI->>C: messages.create() with tools

    alt Claude decides to search
        C-->>AI: tool_use request
        AI->>T: execute_tool()
        T->>V: search()
        V->>V: Embed query
        V->>V: Search ChromaDB
        V-->>T: Search results
        T->>T: Format results
        T-->>AI: Formatted results
        AI->>C: messages.create() with results
        C-->>AI: Final response
    else Use general knowledge
        C-->>AI: Direct response
    end

    AI-->>R: Generated response
    R->>T: get_last_sources()
    T-->>R: Sources list
    R->>R: Update history
    R-->>A: response and sources

    A-->>F: JSON response
    F->>F: Remove loading
    F->>F: Add message
    F->>F: Add sources
    F-->>U: Display response
```

## Component Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web UI<br/>index.html]
        JS[JavaScript<br/>script.js]
        CSS[Styling<br/>style.css]
    end

    subgraph "API Layer"
        FastAPI[FastAPI Server<br/>app.py]
        Models[Pydantic Models<br/>models.py]
        Config[Configuration<br/>config.py]
    end

    subgraph "RAG Core"
        RAGSys[RAG System<br/>rag_system.py]
        SessionMgr[Session Manager<br/>session_manager.py]
    end

    subgraph "AI & Search"
        AIGen[AI Generator<br/>ai_generator.py]
        Tools[Tool Manager<br/>search_tools.py]
        SearchTool[Course Search Tool]
    end

    subgraph "Data Layer"
        VectorStore[Vector Store<br/>vector_store.py]
        DocProcessor[Document Processor<br/>document_processor.py]
        ChromaDB[(ChromaDB<br/>Vector Database)]
        CourseFiles[(Course Files<br/>docs/*.txt)]
    end

    subgraph "External APIs"
        ClaudeAPI[Anthropic Claude API]
        Embeddings[Sentence Transformers<br/>Embeddings]
    end

    %% User interaction flow
    UI --> JS
    JS --> FastAPI

    %% API to RAG flow
    FastAPI --> RAGSys
    FastAPI --> Models
    FastAPI --> Config

    %% RAG orchestration
    RAGSys --> AIGen
    RAGSys --> SessionMgr
    RAGSys --> Tools

    %% AI and tool execution
    AIGen --> ClaudeAPI
    AIGen --> Tools
    Tools --> SearchTool
    SearchTool --> VectorStore

    %% Data processing and storage
    VectorStore --> ChromaDB
    VectorStore --> Embeddings
    DocProcessor --> CourseFiles
    DocProcessor --> VectorStore

    %% Styling
    classDef frontend fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef rag fill:#e8f5e8
    classDef ai fill:#fff3e0
    classDef data fill:#fce4ec
    classDef external fill:#f1f8e9

    class UI,JS,CSS frontend
    class FastAPI,Models,Config api
    class RAGSys,SessionMgr rag
    class AIGen,Tools,SearchTool ai
    class VectorStore,DocProcessor,ChromaDB,CourseFiles data
    class ClaudeAPI,Embeddings external
```

## Data Flow Summary

1. **User Input** → Frontend captures and validates
2. **HTTP Request** → FastAPI receives and routes
3. **RAG Orchestration** → Coordinates all components
4. **AI Decision** → Claude determines if search is needed
5. **Tool Execution** → Semantic search in vector database
6. **Response Synthesis** → Claude combines search results
7. **UI Update** → Display response with sources

## Key Technologies

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Python FastAPI, Pydantic
- **AI**: Anthropic Claude API with tool calling
- **Vector DB**: ChromaDB with sentence-transformers
- **Search**: Semantic similarity matching
- **Session**: In-memory conversation history
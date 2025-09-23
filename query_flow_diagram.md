# RAG System Query Processing Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Frontend<br/>(script.js)
    participant API as FastAPI<br/>(app.py)
    participant RAG as RAGSystem<br/>(rag_system.py)
    participant AI as AIGenerator<br/>(ai_generator.py)
    participant Tools as ToolManager<br/>(search_tools.py)
    participant Vector as VectorStore<br/>(vector_store.py)
    participant Claude as Anthropic<br/>Claude API

    User->>Frontend: Types query & clicks send
    Frontend->>Frontend: Disable UI, show loading
    Frontend->>API: POST /api/query<br/>{query, session_id}

    API->>API: Create session if needed
    API->>RAG: rag_system.query(query, session_id)

    RAG->>RAG: Build prompt:<br/>"Answer this question about course materials: {query}"
    RAG->>RAG: Get conversation history
    RAG->>AI: generate_response(prompt, history, tools, tool_manager)

    AI->>AI: Build system prompt + context
    AI->>Claude: messages.create() with tools enabled

    alt Claude decides to use search tool
        Claude-->>AI: tool_use: search_course_content
        AI->>Tools: execute_tool("search_course_content", query, filters)
        Tools->>Vector: search(query, course_name, lesson_number)
        Vector->>Vector: Embed query with sentence-transformers
        Vector->>Vector: Search ChromaDB collections
        Vector-->>Tools: SearchResults with documents & metadata
        Tools->>Tools: Format results + store sources
        Tools-->>AI: Formatted search results
        AI->>Claude: messages.create() with tool results
        Claude-->>AI: Final synthesized response
    else Claude uses general knowledge
        Claude-->>AI: Direct response without tools
    end

    AI-->>RAG: Generated response text
    RAG->>Tools: get_last_sources()
    Tools-->>RAG: Sources list
    RAG->>RAG: Update conversation history
    RAG-->>API: (response, sources)

    API-->>Frontend: JSON response<br/>{answer, sources, session_id}
    Frontend->>Frontend: Remove loading spinner
    Frontend->>Frontend: Add message with markdown
    Frontend->>Frontend: Add collapsible sources
    Frontend->>Frontend: Re-enable UI, scroll down
    Frontend-->>User: Display response with sources
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
"""Architecture diagrams (Mermaid) for teaching."""

SYSTEM_ARCHITECTURE = """
```mermaid
flowchart TB
    subgraph Client["Student Browser"]
        UI[Streamlit UI app.py]
    end

    subgraph Config["Configuration Layer"]
        ENV[.env / BYOK Keys]
        OPT[GenerationOptions<br/>temperature, max_tokens, model]
        CAT[Modality Catalog<br/>best model hints]
    end

    subgraph Services["Service Layer src/services/"]
        TXT[text.py]
        IMG[image.py]
        AUD[audio.py]
        VID[video.py]
        GEM[gemini.py]
        ANT[anthropic.py]
        HF[huggingface.py]
    end

    subgraph Providers["External APIs"]
        OAI[OpenAI]
        GEMINI[Google Gemini]
        GROQ[Groq]
        OR[OpenRouter]
        CLAUDE[Anthropic]
        HFAPI[HF Inference]
        OLL[Ollama Local]
    end

    UI --> ENV
    UI --> OPT
    UI --> CAT
    UI --> TXT
    UI --> IMG
    UI --> AUD
    UI --> VID
    TXT --> GEM
    TXT --> ANT
    TXT --> HF
    TXT --> OAI
    TXT --> GROQ
    TXT --> OR
    TXT --> OLL
    IMG --> OAI
    IMG --> HF
    IMG --> GEM
    IMG --> ANT
    VID --> GEM
    VID --> ANT
    VID --> HF
```
"""

LANGCHAIN_ARCHITECTURE = """
```mermaid
flowchart LR
    subgraph LCEL["LangChain LCEL"]
        P[ChatPromptTemplate]
        M[ChatModel<br/>ChatOpenAI / ChatAnthropic / ...]
        PAR[StrOutputParser]
        P --> M --> PAR
    end

    subgraph Runnable["Runnable Interface"]
        INV[invoke]
        STR[stream]
        BAT[batch]
    end

    PAR --> INV
    M --> Runnable

    subgraph Memory["Optional Extensions"]
        MEM[ConversationBufferMemory]
        RET[RAG Retriever]
        AGT[Agents + Tools]
    end

    M -.-> MEM
    M -.-> RET
    M -.-> AGT
```
"""

MODALITY_FLOWS: dict[str, str] = {
    "text_to_text": """
```mermaid
sequenceDiagram
    participant S as Student
    participant ST as Streamlit
    participant SVC as chat_completion()
    participant API as Provider API

    S->>ST: Enter prompt + click Generate
    ST->>SVC: prompt, provider, keys, options
    SVC->>API: Chat completion request
    API-->>SVC: Response text
    SVC-->>ST: text, model_id
    ST-->>S: Markdown answer
```
""",
    "image_to_text": """
```mermaid
sequenceDiagram
    participant S as Student
    participant ST as Streamlit
    participant SVC as analyze_image()
    participant API as Vision API

    S->>ST: Upload image + optional question
    ST->>SVC: image_bytes, prompt, provider
    SVC->>API: Multimodal message image+text
    API-->>SVC: Description / answer
    SVC-->>ST: result
    ST-->>S: Image + text side by side
```
""",
    "video_to_text": """
```mermaid
flowchart LR
    V[Video bytes] --> CV[OpenCV extract 6 frames]
    CV --> F1[Frame 1]
    CV --> F2[Frame 2]
    CV --> FN[Frame N]
    F1 --> LLM[Vision LLM]
    F2 --> LLM
    FN --> LLM
  LLM --> SUM[Summary text]
```
""",
    "text_to_image": """
```mermaid
flowchart LR
    T[Text prompt] --> GEN[generate_image]
    GEN --> OAI[DALL-E 3]
    GEN --> HF[Stable Diffusion XL]
    OAI --> BYTES[PNG bytes]
    HF --> BYTES
    BYTES --> UI[st.image]
```
""",
    "audio_to_text": """
```mermaid
flowchart LR
    A[Audio upload] --> STT[transcribe_audio]
    STT --> W[Whisper OpenAI]
    STT --> G[Gemini audio]
    STT --> H[HF Whisper]
    W --> TXT[Transcript]
    G --> TXT
    H --> TXT
```
""",
}


def get_system_architecture() -> str:
    return SYSTEM_ARCHITECTURE.strip()


def get_langchain_architecture() -> str:
    return LANGCHAIN_ARCHITECTURE.strip()


def get_modality_flow(modality_id: str) -> str:
    return MODALITY_FLOWS.get(modality_id, MODALITY_FLOWS["text_to_text"]).strip()

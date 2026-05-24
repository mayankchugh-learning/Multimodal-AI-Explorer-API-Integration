"""Architecture diagrams (Mermaid + ASCII) for teaching."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectureDiagram:
    title: str
    mermaid: str
    ascii: str


SYSTEM = ArchitectureDiagram(
    title="Full application system",
    mermaid="""flowchart TB
    subgraph Client["Student Browser"]
        UI[Streamlit UI app.py]
    end
    subgraph Config["Configuration"]
        ENV[.env and BYOK keys]
        OPT[GenerationOptions]
        CAT[Modality catalog]
    end
    subgraph Services["src/services"]
        TXT[text.py]
        IMG[image.py]
        AUD[audio.py]
        VID[video.py]
    end
    subgraph APIs["External providers"]
        OAI[OpenAI]
        GEM[Google Gemini]
        GROQ[Groq]
        OR[OpenRouter]
        ANT[Anthropic]
        HF[Hugging Face]
        OLL[Ollama]
    end
    UI --> ENV
    UI --> OPT
    UI --> CAT
    UI --> TXT
    UI --> IMG
    UI --> AUD
    UI --> VID
    TXT --> OAI
    TXT --> GEM
    TXT --> GROQ
    TXT --> OR
    TXT --> ANT
    TXT --> HF
    TXT --> OLL
    IMG --> OAI
    IMG --> HF
    VID --> GEM
    VID --> ANT""",
    ascii="""┌─────────────────────────────────────────────────────────┐
│                    STUDENT (Browser)                     │
│                     Streamlit UI (app.py)                │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   .env / BYOK        GenerationOptions    Modality catalog
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
              ┌─────────────────────────────┐
              │   src/services/             │
              │ text | image | audio | video│
              └─────────────┬───────────────┘
                            ▼
    OpenAI · Gemini · Groq · OpenRouter · Anthropic · HF · Ollama
""",
)

LANGCHAIN = ArchitectureDiagram(
    title="LangChain LCEL stack",
    mermaid="""flowchart LR
    subgraph Chain["LCEL chain"]
        P[ChatPromptTemplate]
        M[ChatModel]
        R[StrOutputParser]
        P --> M --> R
    end
    subgraph Models["ChatModel examples"]
        OAI[ChatOpenAI]
        ANT[ChatAnthropic]
        GEM[ChatGoogleGenerativeAI]
        GR[ChatGroq]
        OL[ChatOllama]
    end
    M --> Models
    subgraph Extra["Optional"]
        MEM[Memory]
        RET[RAG retriever]
        AGT[Agents + tools]
    end
    M -.-> Extra""",
    ascii="""  ChatPromptTemplate  ──►  ChatModel  ──►  StrOutputParser
        │                      │                    │
   {question}            provider SDK           plain text
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ChatOpenAI    ChatAnthropic    ChatGoogleGenerativeAI
              │               │               │
         (+ Groq, Ollama, HuggingFace, OpenRouter base_url)
""",
)

MODALITY_DIAGRAMS: dict[str, ArchitectureDiagram] = {
    "text_to_text": ArchitectureDiagram(
        title="Text → Text flow",
        mermaid="""sequenceDiagram
    participant S as Student
    participant ST as Streamlit
    participant SVC as chat_completion
    participant API as Provider API
    S->>ST: Enter prompt
    ST->>SVC: prompt + provider + options
    SVC->>API: Chat request
    API-->>SVC: Response
    SVC-->>ST: text + model name
    ST-->>S: Display answer""",
        ascii="""  Student          Streamlit           Service           API
     │                 │                    │                │
     │  type prompt    │                    │                │
     │────────────────►│                    │                │
     │                 │ chat_completion()  │                │
     │                 │───────────────────►│                │
     │                 │                    │  HTTP request  │
     │                 │                    │───────────────►│
     │                 │                    │◄───────────────│
     │                 │◄───────────────────│   response     │
     │◄────────────────│  show markdown   │                │
""",
    ),
    "text_to_image": ArchitectureDiagram(
        title="Text → Image flow",
        mermaid="""flowchart LR
    T[Text prompt] --> G[generate_image]
    G --> OAI[DALL-E 3 OpenAI]
    G --> HF[SDXL Hugging Face]
    OAI --> B[Image bytes]
    HF --> B
    B --> UI[st.image display]""",
        ascii="""  [Text prompt] ──► generate_image() ──┬──► OpenAI DALL-E 3
                                              └──► HF Stable Diffusion XL
                                                        │
                                                        ▼
                                                  [PNG bytes] ──► st.image()
""",
    ),
    "image_to_text": ArchitectureDiagram(
        title="Image → Text flow",
        mermaid="""sequenceDiagram
    participant S as Student
    participant ST as Streamlit
    participant SVC as analyze_image
    participant API as Vision API
    S->>ST: Upload image
    ST->>SVC: bytes + question
    SVC->>API: Image + text multimodal
    API-->>SVC: Description
    SVC-->>ST: result
    ST-->>S: Image and text""",
        ascii="""  [Upload image] ──► analyze_image() ──► Vision API
                           │                    (GPT / Claude / Gemini / BLIP)
                           ▼
                    Description shown next to image
""",
    ),
    "text_to_audio": ArchitectureDiagram(
        title="Text → Audio flow",
        mermaid="""flowchart LR
    T[Text input] --> TTS[generate_speech]
    TTS --> OAI[OpenAI TTS tts-1]
    OAI --> MP3[MP3 bytes]
    MP3 --> A[st.audio player]""",
        ascii="""  [Text] ──► generate_speech() ──► OpenAI audio.speech (tts-1)
                                              │
                                              ▼
                                         [MP3] ──► st.audio()
""",
    ),
    "audio_to_text": ArchitectureDiagram(
        title="Audio → Text flow",
        mermaid="""flowchart LR
    A[Audio file or mic] --> STT[transcribe_audio]
    STT --> W[Whisper OpenAI]
    STT --> G[Gemini audio]
    STT --> H[HF Whisper]
    W --> T[Transcript text]
    G --> T
    H --> T""",
        ascii="""  [Upload / Record] ──► transcribe_audio() ──┬──► Whisper (OpenAI)
                                                    ├──► Gemini multimodal
                                                    └──► HF whisper-large-v3
                                                              │
                                                              ▼
                                                        [Transcript]
""",
    ),
    "video_to_text": ArchitectureDiagram(
        title="Video → Text flow",
        mermaid="""flowchart TB
    V[Video upload] --> CV[OpenCV sample frames]
    CV --> F1[Frame 1]
    CV --> F2[Frame 2]
    CV --> FN[Frame N]
    F1 --> LLM[Vision LLM]
    F2 --> LLM
    FN --> LLM
    LLM --> SUM[Summary text]""",
        ascii="""  [Video.mp4] ──► OpenCV (6 key frames)
              │
              ├── frame_1 ──┐
              ├── frame_2 ──┼──► Vision model (GPT / Claude / Gemini / BLIP+LLM)
              └── frame_N ──┘
                              │
                              ▼
                        [Video summary text]
""",
    ),
    "text_to_video": ArchitectureDiagram(
        title="Text → Video (conceptual)",
        mermaid="""flowchart LR
    T[Text prompt] --> AGT[LangChain Agent]
    AGT --> TOOL[generate_video tool]
    TOOL --> API[Runway / Veo / Sora API]
    API --> JOB[Async video job]
    JOB --> MP4[MP4 URL]""",
        ascii="""  [Text idea] ──► Agent + @tool ──► External Video API
                                      │
                                      ▼
                               (job polling) ──► MP4 URL
  Note: This demo shows API guidance only; wire paid APIs in production.
""",
    ),
}


def get_system_diagram() -> ArchitectureDiagram:
    return SYSTEM


def get_langchain_diagram() -> ArchitectureDiagram:
    return LANGCHAIN


def get_modality_diagram(modality_id: str) -> ArchitectureDiagram:
    return MODALITY_DIAGRAMS.get(modality_id, MODALITY_DIAGRAMS["text_to_text"])


# Back-compat helpers (markdown fenced) for docs
def get_system_architecture() -> str:
    d = SYSTEM
    return f"```mermaid\n{d.mermaid}\n```"


def get_langchain_architecture() -> str:
    d = LANGCHAIN
    return f"```mermaid\n{d.mermaid}\n```"


def get_modality_flow(modality_id: str) -> str:
    d = get_modality_diagram(modality_id)
    return f"```mermaid\n{d.mermaid}\n```"

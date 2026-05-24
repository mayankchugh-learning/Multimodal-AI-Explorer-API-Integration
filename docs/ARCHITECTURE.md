# Multimodal AI Explorer — Architecture (Teaching Guide)

## Layered design

| Layer | Folder | Responsibility |
|-------|--------|----------------|
| UI | `app.py` | Streamlit tabs, BYOK, recommendations, **Learn panels** |
| Education | `src/education/` | Logic steps, LangChain snippets, Mermaid diagrams |
| Services | `src/services/` | Provider adapters per modality |
| Config | `src/config.py` | API keys from `.env` + BYOK merge |
| Catalog | `src/modality_catalog.py` | Best-model hints per task |

## Request flow (Text → Text)

1. Student enters prompt in Streamlit.
2. `GenerationOptions` captures temperature, max_tokens, model.
3. `chat_completion()` in `src/services/text.py` routes by `provider`.
4. Provider SDK returns text → displayed in UI.

## LangChain mapping (what students should learn)

| This app calls | LangChain equivalent |
|----------------|---------------------|
| `openai.chat.completions` | `ChatOpenAI` + LCEL `\|` chain |
| `anthropic.messages.create` | `ChatAnthropic` |
| `google.genai` generate_content | `ChatGoogleGenerativeAI` |
| `groq.chat.completions` | `ChatGroq` |
| `InferenceClient.chat_completion` | `ChatHuggingFace` + `HuggingFaceEndpoint` |
| OpenAI-compatible Ollama URL | `ChatOllama` |

**LCEL pattern:**

```text
prompt | chat_model | output_parser
```

## Multimodal patterns

- **Image → Text:** Multimodal message = text block + image (base64 or URL).
- **Video → Text:** Pre-process video → frames → same as multi-image vision.
- **Audio → Text:** File upload → Whisper or Gemini audio `Part`.

## Student exercises

1. Copy a **LangChain** snippet from the app Learn panel into a notebook.
2. Replace hardcoded prompts with `ChatPromptTemplate` variables.
3. Add `ConversationBufferMemory` for multi-turn chat.
4. Wrap `analyze_image` logic in a `@tool` for a LangChain agent.

See `requirements-langchain.txt` for install list.

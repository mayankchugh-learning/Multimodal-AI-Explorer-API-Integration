"""API key reference data for UI and documentation."""

from __future__ import annotations

from typing import TypedDict


class ApiKeyRow(TypedDict):
    Provider: str
    Get_key_at: str
    Env_variable: str
    Notes: str


API_KEY_ROWS: list[ApiKeyRow] = [
    {
        "Provider": "OpenAI",
        "Get_key_at": "https://platform.openai.com/api-keys",
        "Env_variable": "OPENAI_API_KEY",
        "Notes": "Chat, DALL-E, Whisper, TTS",
    },
    {
        "Provider": "Anthropic",
        "Get_key_at": "https://platform.claude.com/docs/en/api/admin/api_keys/retrieve",
        "Env_variable": "ANTHROPIC_API_KEY",
        "Notes": "Claude text + vision",
    },
    {
        "Provider": "Groq",
        "Get_key_at": "https://console.groq.com/",
        "Env_variable": "GROQ_API_KEY",
        "Notes": "Fast Llama inference",
    },
    {
        "Provider": "OpenRouter",
        "Get_key_at": "https://openrouter.ai/workspaces/default/keys",
        "Env_variable": "OPENROUTER_API_KEY",
        "Notes": "100+ routed models",
    },
    {
        "Provider": "Hugging Face",
        "Get_key_at": "https://huggingface.co/settings/tokens",
        "Env_variable": "HUGGINGFACEHUB_API_TOKEN",
        "Notes": "Also: HUGGINGFACE_API_KEY, HF_TOKEN",
    },
    {
        "Provider": "Gemini",
        "Get_key_at": "https://ai.google.dev/gemini-api/docs/api-key",
        "Env_variable": "GOOGLE_API_KEY",
        "Notes": "Also: GEMINI_API_KEY",
    },
    {
        "Provider": "Ollama (local)",
        "Get_key_at": "https://ollama.com/",
        "Env_variable": "OLLAMA_BASE_URL",
        "Notes": "No key; default http://localhost:11434/v1",
    },
    {
        "Provider": "LangSmith",
        "Get_key_at": "https://smith.langchain.com/settings",
        "Env_variable": "LANGCHAIN_API_KEY",
        "Notes": "Optional — tracing only (not required)",
    },
]


def rows_for_display() -> list[dict[str, str]]:
    return [
        {
            "Provider": r["Provider"],
            "Get key at": r["Get_key_at"],
            "Env variable": r["Env_variable"],
            "Notes": r["Notes"],
        }
        for r in API_KEY_ROWS
    ]

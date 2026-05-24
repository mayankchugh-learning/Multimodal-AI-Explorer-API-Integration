"""Render API key reference tables in Streamlit."""

import streamlit as st

from src.api_key_reference import rows_for_display


def render_api_key_tables() -> None:
    st.markdown("### API keys → typical `.env` names")
    st.caption("Copy variable names into a `.env` file in the project root, or use BYOK above.")

    st.dataframe(
        rows_for_display(),
        width="stretch",
        hide_index=True,
        column_config={
            "Get key at": st.column_config.LinkColumn("Get key at", display_text="Open"),
        },
    )

    st.markdown("**Example `.env` snippet**")
    st.code(
        """OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
HUGGINGFACEHUB_API_TOKEN=hf_...
GOOGLE_API_KEY=AIza...
OLLAMA_BASE_URL=http://localhost:11434/v1
# LANGCHAIN_API_KEY=lsv2_...  # optional tracing""",
        language="bash",
    )

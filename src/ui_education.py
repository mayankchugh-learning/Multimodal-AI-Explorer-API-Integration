"""Streamlit UI for student learning panels."""

import streamlit as st

from src.education.architecture import (
    get_langchain_architecture,
    get_modality_flow,
    get_system_architecture,
)
from src.education.implementation_logic import get_logic_steps, get_provider_note
from src.education.langchain_examples import get_langchain_code
from src.modality_catalog import get_modality


def render_learning_panel(
    modality_id: str,
    provider: str,
    model_override: str | None,
    *,
    key_prefix: str = "learn",
) -> None:
    """Show implementation logic, LangChain code, and architecture for current selection."""
    modality = get_modality(modality_id)

    with st.expander(f"🎓 Learn: {modality.label} — Logic, LangChain & Architecture", expanded=False):
        tab_logic, tab_lc, tab_arch = st.tabs(
            ["Implementation logic", "LangChain code", "Architecture"]
        )

        with tab_logic:
            st.markdown(f"**Task:** {modality.label}")
            st.caption(modality.description)
            st.markdown("**General pipeline (this app)**")
            for step in get_logic_steps(modality_id):
                st.markdown(f"- {step}")
            st.markdown("**Provider-specific adapter**")
            st.info(get_provider_note(modality_id, provider))
            st.markdown(
                f"**Your selection:** provider=`{provider}`, "
                f"model=`{model_override or '(default)'}`"
            )

        with tab_lc:
            st.markdown("**LangChain example** (copy into a `.py` file or notebook)")
            st.caption(
                "Install packages shown in the snippet header. "
                "See `requirements-langchain.txt` in the project root."
            )
            code = get_langchain_code(modality_id, provider, model_override)
            st.code(code, language="python")
            st.download_button(
                "Download snippet (.py)",
                data=code,
                file_name=f"langchain_{modality_id}_{provider}.py",
                mime="text/x-python",
                key=f"{key_prefix}_dl_{modality_id}_{provider}",
            )

        with tab_arch:
            st.markdown("**This modality — data flow**")
            st.markdown(get_modality_flow(modality_id))
            with st.expander("Full app system architecture"):
                st.markdown(get_system_architecture())
            with st.expander("LangChain LCEL architecture"):
                st.markdown(get_langchain_architecture())

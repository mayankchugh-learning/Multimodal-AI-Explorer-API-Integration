"""Streamlit UI for modality-based model recommendations."""

import streamlit as st

from src.config import ProviderKeys
from src.modality_catalog import (
    RATING_LABEL,
    ModelRecommendation,
    _provider_ready,
    best_for_modality,
    get_modality,
    list_modalities,
)


def apply_recommendation(rec: ModelRecommendation) -> None:
    st.session_state.provider = rec.provider
    if rec.model and rec.model != "—":
        st.session_state.model_override = rec.model.split(" (")[0].strip()


def render_modality_recommendations(
    modality_id: str,
    keys: ProviderKeys,
    current_provider: str,
    *,
    key_prefix: str = "main",
    show_apply_button: bool = True,
    show_provider_table: bool = True,
) -> None:
    modality = get_modality(modality_id)
    best = best_for_modality(modality_id, keys)

    if best:
        st.success(
            f"**Recommended:** **{best.provider_label}** → `{best.model}` — {best.note}"
        )
    else:
        st.warning(
            "No API key for a recommended provider. Add keys in **BYOK** or `.env`."
        )

    if current_provider:
        match = next((m for m in modality.models if m.provider == current_provider), None)
        if match and match.rating == "best":
            st.info(f"Selected **{match.provider_label}** is ⭐ **Best** for {modality.label}.")
        elif match and match.rating == "unsupported":
            st.error(
                f"**{match.provider_label}** is **not supported** for {modality.label}. "
                "Switch provider using the buttons below."
            )
        elif match and match.rating == "good":
            st.info(f"**{match.provider_label}** is a good fit ({RATING_LABEL[match.rating]}).")

    if show_provider_table:
        with st.expander(
            f"📋 All providers & models — {modality.label}",
            expanded=False,
        ):
            st.caption(modality.description)
            rows = []
            for m in modality.models:
                rows.append(
                    {
                        "Rating": RATING_LABEL[m.rating],
                        "Provider": m.provider_label,
                        "Model": m.model,
                        "Key ready": "✅" if _provider_ready(m.provider, keys) else "❌",
                        "Notes": m.note,
                    }
                )
            st.dataframe(rows, width="stretch", hide_index=True)

            if show_apply_button and modality.best_options():
                st.markdown("**Apply a ⭐ best pick**")
                best_opts = modality.best_options()
                cols = st.columns(min(len(best_opts), 3))
                for i, rec in enumerate(best_opts):
                    with cols[i % len(cols)]:
                        btn_key = f"{key_prefix}_apply_{modality_id}_{rec.provider}_{i}"
                        if st.button(
                            rec.provider_label,
                            key=btn_key,
                            disabled=not _provider_ready(rec.provider, keys),
                            width="stretch",
                            help=rec.model,
                        ):
                            apply_recommendation(rec)
                            st.rerun()


def render_sidebar_modality_picker(keys: ProviderKeys, current_provider: str) -> None:
    st.subheader("Task guide")
    modality_labels = {m.id: m.label for m in list_modalities()}
    selected_id = st.selectbox(
        "Browse by modality",
        options=list(modality_labels.keys()),
        format_func=lambda x: modality_labels[x],
        key="sidebar_modality",
    )
    render_modality_recommendations(
        selected_id,
        keys,
        current_provider,
        key_prefix="sidebar",
        show_apply_button=False,
        show_provider_table=False,
    )
